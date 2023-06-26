import os
import traceback

from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from refactor_output import refactor_output
from langchain.vectorstores import Chroma
from prompts import MATCHED_VC_NAMES_PROMPT
from langchain.chains import RetrievalQA
from get_info_about_fund import get_info_about_fund
from langchain.chat_models import ChatOpenAI
import openai
import time
import random


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
        loader = CSVLoader(file_path='csvs/new_data.csv', csv_args={
            'delimiter': ',',
            'fieldnames': [
                'vc_name', 'vc_website_url', 'vc_linkedin_url', 'vc_investor_name',
                'vc_investor_email', 'vc_stages', 'vc_industries',
                'vc_portfolio_startup_name', 'vc_portfolio_startup_website_url',
                'vc_portfolio_startup_solution'
            ]
        })

        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=14000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory="test_chroma_save")

        # embeddings = OpenAIEmbeddings()
        # docsearch = Chroma(persist_directory="chroma_save", embedding_function=embeddings)

        # Create the question answering model
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0
        )
        qa = RetrievalQA.from_llm(llm=llm, retriever=docsearch.as_retriever(), prompt=MATCHED_VC_NAMES_PROMPT)

        # Ask a question and get an answer
        answer = qa.run(query=query)
        print(answer)
        return answer
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None


def main():
    print("Bot is ready to chat. Type 'exit' to stop chatting.")

    # startup_name = input("Enter the startup name: ")
    # startup_industry = input("Enter the startup industry: ")
    # startup_stage = input("Enter the startup stage: ")
    # problems_solved = input("Enter the problems solved by the startup: ")

    # startup_name = "Debonne"
    # startup_industry = "Healthcare"
    # startup_stage = "Seed"
    # problems_solved = "It produces pills for third party countries"

    startup_name = "Juko"
    startup_industry = "Finance, automation, money"
    startup_stage = "Seed"
    problems_solved = "It solves the user problem of automating key areas of business operations such as invoicing, payment collections, bulk payouts, GST filing, and customer data management."

    # startup_name = "SIRPLUS"
    # startup_industry = "B2C, Ecommerce, Climate Tech"
    # startup_stage = "Seed"
    # problems_solved = "It helps consumer to buy let over food from store at an attractive price to help reduce foodwaste and save the planet"

    query = f"{startup_name} is a startup that works at {startup_stage} stage(s) in the {startup_industry} industry(s) that solves the following problems: {problems_solved}."
    funds = get_matched_fund_names(query)

    if funds.startswith("Sorry, try again"):
        print(funds)
    else:
        fund_names = funds.split(", ")
        for fund_name in fund_names:
            if fund_name.startswith("these are all the funds that are likely to invest in the startup"):
                print(fund_name)
            else:
                raw_info = get_info_about_fund(fund_name, query)
                info = refactor_output(raw_info)

                print(info)


if __name__ == '__main__':
    main()
