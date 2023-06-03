from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
import openai
import time
import random

#
# def retry_with_exponential_backoff(
#         func,
#         initial_delay: float = 1,
#         exponential_base: float = 2,
#         jitter: bool = True,
#         max_retries: int = 10,
#         errors: tuple = (openai.error.RateLimitError,),
# ):
#     """Retry a function with exponential backoff."""
#
#     def wrapper(*args, **kwargs):
#         # Initialize variables
#         num_retries = 0
#         delay = initial_delay
#
#         # Loop until a successful response or max_retries is hit or an exception is raised
#         while True:
#             try:
#                 return func(*args, **kwargs)
#
#             # Retry on specific errors
#             except errors as e:
#                 # Increment retries
#                 num_retries += 1
#
#                 # Check if max retries has been reached
#                 if num_retries > max_retries:
#                     raise Exception(
#                         f"Maximum number of retries ({max_retries}) exceeded."
#                     )
#
#                 # Increment the delay
#                 delay *= exponential_base * (1 + jitter * random.random())
#
#                 # Sleep for the delay
#                 time.sleep(delay)
#
#             # Raise exceptions for any errors not specified
#             except Exception as e:
#                 raise e
#
#     return wrapper
#
#
# @retry_with_exponential_backoff


async def gpt_info_via_text(text, question):
    res = "I don't know"
    template = """You are a very good analyst of startups. Answer task below based on context information below. Don't try to make up answer. If you not sure about the answer just write "I don't know"
Task: {question}

Context:
{context}

Your answer:
"""

    prompt = PromptTemplate(template=template, input_variables=["question", "context"])

    llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
        )

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    question = question
    context = text

    res = await llm_chain.arun({'question': question, 'context': context})

    return res

