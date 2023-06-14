import traceback

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from prompts import LAST_ANSWER_PROMPT
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
def get_info_about_fund(fund_name, startup_info):
    try:
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma(persist_directory="chroma_save", embedding_function=embeddings)

        # Create the question answering model
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0
        )
        qa = RetrievalQA.from_llm(llm=llm, retriever=docsearch.as_retriever(), prompt=LAST_ANSWER_PROMPT)

        query = f"""NAME OF CERTAIN FUND:
    {fund_name}
    
    USER'S STARTUP INFORMATION:
    {startup_info}"""

        # Ask a question and get an answer
        answer = qa.run(query=query)
        return answer
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None



if __name__ == '__main__':
    get_info_about_fund()
