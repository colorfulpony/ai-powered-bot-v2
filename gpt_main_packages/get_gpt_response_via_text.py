from langchain import OpenAI
from langchain.output_parsers import StructuredOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.vectorstores import Chroma
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
def gpt_info_via_text(cleaned_text, response_schemas, question):
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

    # text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', ' ', '.', ',', ''],
        chunk_size=500,
        chunk_overlap=80
    )
    split_text = text_splitter.split_text(cleaned_text)

    # embeddings
    embeddings = OpenAIEmbeddings()

    # vector store
    docsearch = Chroma.from_texts(
        split_text,
        embeddings,
        metadatas=[{"source": str(i)} for i in range(len(split_text))]
    )

    # chain
    qa_chain = load_qa_with_sources_chain(
        ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo"
        ),
        chain_type="map_rerank"
    )

    qa = RetrievalQAWithSourcesChain(
        combine_documents_chain=qa_chain,
        retriever=docsearch.as_retriever(),
        reduce_k_below_max_tokens=True
    )

    res = qa({"question": _input.to_messages()[0].content + "\n" + _input.to_messages()[1].content})

    return res["answer"]

