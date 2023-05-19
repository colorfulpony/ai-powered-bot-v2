from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
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

from clean_text_after_scrapping.clean_text_after_scrape import clean_text
from website_scrapping.vc_website_scrape import scrape_website


@retry_with_exponential_backoff
def gpt_info(url, response_schemas, question):
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    # prompt
    prompt_template = """Answer the following question with a comma-separated list of things for the answer.  If you don't know the anwer - just write "-". Don't make up answer.
    \n=====================
    \nQuestion: {question}
    \n=====================
    \nYour answer:"""

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template("Your are an invest fund analyst"),
            HumanMessagePromptTemplate.from_template(prompt_template)
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    _input = prompt.format_prompt(question=question)

    raw_text = scrape_website(url)
    cleaned_text = clean_text(raw_text)

    # text splitter
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=500, chunk_overlap=80)
    split_text = text_splitter.split_text(cleaned_text)

    # embeddings
    embeddings = OpenAIEmbeddings()

    # vector store
    vectorstore = FAISS.from_texts(split_text, embeddings, metadatas=[{"source": f"{i}-pl"} for i in range(len(split_text))])
    # vectorstore.save_local("faiss_index")
    # new_vectorestore = FAISS.load_local("faiss_index", embeddings)

    # chain
    chain_type_kwargs = {"question_prompt ": _input.to_messages()[0].content + "\n" + _input.to_messages()[1].content}
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=ChatOpenAI(
            temperature=0,
            model_name="gpt_main_packages-3.5-turbo",
        ),
        chain_type="refine",
        retriever=vectorstore.as_retriever(),
        reduce_k_below_max_tokens=True,
    )

    res = chain({"question": _input.to_messages()[0].content + "\n" + _input.to_messages()[1].content})

    return res['answer']

