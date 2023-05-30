from langchain import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
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
def get_last_response(startup_info, fund_name, docsearch):
    response_schemas = [
        ResponseSchema(name="Fund name", description="Write name of the investment fund"),
        ResponseSchema(name="Fund website", description="Write the website url of the investment fund"),
        ResponseSchema(name="Analyst name", description="Write name of the analyst of the investment fund"),
        ResponseSchema(name="Analyst linkedin", description="Write linkedin url of the analyst of the investment fund"),
        ResponseSchema(name="Individual email message", description="Personalized email to an investment fund analyst. An email that a user can use to get an investment from this fund. One of the sentences should be about 1-2 startup(s) that this investment fund has invested in before (but only include those that solve very similar problems and are in the same industry as the user's startup). Be sure to include the name and website url of the startup(s) in which the investment fund has invested in the following form {StartupName(startupname.com), StartupName2(startupname2.com)}")
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    template = """"Based on the information about the venture funds I gave you, find the best of them that are likely to invest in the described user's startup. Use only funds that I gave you.
    Do not combine information from different funds.
    Do not try to make up an answer.
    ALWAYS return the "SOURCES" part of your answer.
    
    =========
    STARTUP NAME AND STARTUP INFORMATION: 
    {question}
    =========
    
    =========
    {summaries}
    =========
    
    =========
    ANSWER FORMAT:
    \n{format_instructions}
    =========
    
    =========
    YOUR ANSWER:
    """

    PROMPT = PromptTemplate(
        template=template,
        input_variables=["question", "summaries"],
        partial_variables={"format_instructions": format_instructions}
    )

    chain = load_qa_with_sources_chain(
        ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo"),
            chain_type="stuff",
            prompt=PROMPT
    )
    qa = RetrievalQAWithSourcesChain(
        combine_documents_chain=chain,
        retriever=docsearch.as_retriever(),
        reduce_k_below_max_tokens=True
    )

    query = f"""STARTUP
     NAME: {fund_name}
STARTUP DESCRIPTION: {startup_info}"""
    test = qa({"question": query})
    return test["answer"]
