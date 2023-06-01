from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from prompts import MATCHED_VC_NAMES_PROMPT_v2
from langchain.chains import RetrievalQA
from get_last_response_v2 import get_last_response
from langchain.chat_models import ChatOpenAI
import openai
import time
import random


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
def get_matched_fund_names():
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma(persist_directory="chroma_save", embedding_function=embeddings)

    # Create the question answering model
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0
    )
    qa = RetrievalQA.from_llm(llm=llm, retriever=docsearch.as_retriever(), prompt=MATCHED_VC_NAMES_PROMPT_v2)

    print("Bot is ready to chat. Type 'exit' to stop chatting.")
    while True:
        # Prompt user for startup details
        startup_name = input("Enter the startup name: ")
        if startup_name.lower() == "exit":
            break
        startup_industry = input("Enter the startup industry: ")
        if startup_industry.lower() == "exit":
            break
        startup_stage = input("Enter the startup stage: ")
        if startup_stage.lower() == "exit":
            break

        problems_solved = input("Enter the problems solved by the startup: ")
        if problems_solved.lower() == "exit":
            break

        query = f"""{startup_name} is a startup that works at {startup_stage} stage(s) in the {startup_industry} industry(s) that solves the following problems: {problems_solved}."""

        # Ask a question and get an answer
        answer = qa.run(query=query)
        return answer, query


if __name__ == '__main__':
    funds, query = get_matched_fund_names()

    if funds.startswith("Sorry, try again"):
        print(funds)
    else:
        fund_names = funds.split(", ")
        for fund_name in fund_names:
            if fund_name.startswith("No more funds"):
                print(fund_name)
            else:
                info = get_last_response(fund_name, query)
                print(info)
