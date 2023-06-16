import os
import traceback

from langchain import FAISS
from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from refactor_output import refactor_output
from langchain.vectorstores import Chroma
from prompts import MATCHED_VC_NAMES_PROMPT_v6, TEST_PROMPT3
from langchain.chains import RetrievalQA
from get_info_about_fund import get_info_about_fund
from langchain.chat_models import ChatOpenAI
import openai
import time
import random

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Access the API key and use it in API requests
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key


def retry_with_exponential_backoff(
        func,
        initial_delay: float = 1,
        exponential_base: float = 2,
        jitter: bool = True,
        max_retries: int = 10,
        errors: tuple = (openai.error.RateLimitError,),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specific errors
            except errors as e:
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper


@retry_with_exponential_backoff
def get_matched_fund_names(query):
    try:
        loader = CSVLoader(file_path='./new_data.csv', encoding="utf-8", csv_args={
            'delimiter': ',',
            'fieldnames': [
                'vc_name', 'vc_website_url', 'vc_linkedin_url', 'vc_investor_name',
                'vc_investor_email', 'vc_stages', 'vc_industries',
                'vc_portfolio_startup_name', 'vc_portfolio_startup_website_url',
                'vc_portfolio_startup_solution'
            ]
        })

        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=20000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
        )

        # Create the question answering model
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0
        )
        qa = RetrievalQA.from_llm(llm=llm, retriever=docsearch.as_retriever(), prompt=MATCHED_VC_NAMES_PROMPT_v6)

        _input = TEST_PROMPT3.format(subject=query)
        # Ask a question and get an answer
        answer = qa.run(query=_input)
        print(answer)
        return answer
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None


def main():
    # startup_name = input("Enter the startup name: ")
    # startup_industry = input("Enter the startup industry: ")
    # startup_stage = input("Enter the startup stage: ")
    # problems_solved = input("Enter the problems solved by the startup: ")

    startup_name = "Debonne"
    startup_industry = "Healthcare"
    startup_stage = "Seed"
    problems_solved = "It produces pills for third party countries"

    # startup_name = "Juko"
    # startup_industry = "Finance, automation, money"
    # startup_stage = "Seed, early-stage, and Series A"
    # problems_solved = "It solves the user problem of automating key areas of business operations such as invoicing, payment collections, bulk payouts, GST filing, and customer data management."

    # startup_name = "SIRPLUS"
    # startup_industry = "B2C, Ecommerce, Climate Tech"
    # startup_stage = "Seed"
    # problems_solved = "It helps consumer to buy let over food from store at an attractive price to help reduce foodwaste and save the planet"

    # startup_name = "Kol"
    # startup_industry = "AI/ML,B2B,B2C,E-commerce,DTC,Consumer,Edtech,Enterprise Software,FemTech,Foodtech,Future of Work & Productivity,Marketplace,SaaS"
    # startup_stage = "Seed, Series A"
    # problems_solved = "Kol is a startup that provides a powerful AI assistant to help users create content in seconds. It solves the user problem of overcoming writer's block and improving productivity by offering features such as rewriting sentences, fixing grammar and spelling, summarizing lengthy texts, translating in 25+ languages, and generating high-quality content for various purposes such as SEO-optimized blog posts, product descriptions, email copy, ad content, and social media copy. "

    query = f"{startup_name} is a startup that works at {startup_stage} stage in the {startup_industry} industry. {startup_name} startup summary: {problems_solved}."
    funds = get_matched_fund_names(query)


if __name__ == '__main__':
    main()