import traceback

from langchain import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from constants.prompts import LAST_ANSWER
from langchain.chains import RetrievalQA
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
def get_info_about_fund(startup_info, data):
    """
    Get information about a fund based on startup information.

    Parameters:
        startup_info (str): Information about the startup.
        data (dict): Data containing information about the fund.

    Returns:
        str: The answer provided by the model if successful, or None if an error occurs.
    """
    try:
        # Convert the data into a string representation
        data_str = ""
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    data_str += f"{key}: {item}\n"
            else:
                data_str += f"{key}: {value}\n"

        # Create a Document object
        doc = Document(page_content=data_str)

        # Use the document with load_qa_chain
        docs = [doc]

        # Create OpenAI embeddings
        embeddings = OpenAIEmbeddings()

        # Create a FAISS vector store from the documents
        docsearch = FAISS.from_documents(docs, embeddings)

        # Create the question answering model
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0
        )

        # Create a retrieval-based QA model
        qa = RetrievalQA.from_llm(llm=llm, retriever=docsearch.as_retriever(),
                                  prompt=LAST_ANSWER)

        # Ask a question and get an answer
        answer = qa.run(query=startup_info)
        return answer
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None
