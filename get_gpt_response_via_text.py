from langchain import PromptTemplate, LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma


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


# @retry_with_exponential_backoff
async def gpt_info_via_text(cleaned_text, _input):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', ' ', '.', ',', ''], chunk_size=500, chunk_overlap=80
    )
    split_text = text_splitter.split_text(cleaned_text)

    embeddings = OpenAIEmbeddings()

    docsearch = Chroma.from_texts(
        split_text, embeddings, metadatas=[{"source": str(i)} for i in range(len(split_text))]
    )

    qa_chain = load_qa_with_sources_chain(
        ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",), chain_type="map_rerank"
    )

    qa = RetrievalQAWithSourcesChain(
        combine_documents_chain=qa_chain,
        retriever=docsearch.as_retriever(),
        reduce_k_below_max_tokens=True,
    )

    res = qa({"question": _input}, return_only_outputs=True)

    return res['answer']

# async def gpt_info_via_text(text, question):
#     template = """You are a very good analyst of startups. Answer task below based on context information below. Don't try to make up answer. If you not sure about the answer just write "I don't know"
# Task: {question}
#
# Context:
# {context}
#
# Your answer:
# """
#
#     prompt = PromptTemplate(template=template, input_variables=["question", "context"])
#
#     llm = ChatOpenAI(
#         temperature=0,
#         model_name="gpt-3.5-turbo",
#     )
#
#     llm_chain = LLMChain(prompt=prompt, llm=llm)
#
#     question = question
#     context = text
#
#     res = await llm_chain.arun({'question': question, 'context': context})
#
#     print(res)
#     return res
