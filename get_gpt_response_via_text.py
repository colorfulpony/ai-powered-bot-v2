import traceback

from langchain import PromptTemplate, LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma


async def gpt_info_via_text(cleaned_text, _input):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', ' ', '.', ',', ''], chunk_size=500, chunk_overlap=80
        )
        split_text = text_splitter.split_text(cleaned_text)

        embeddings = OpenAIEmbeddings()

        docsearch = Chroma.from_texts(
            split_text, embeddings, metadatas=[{"source": str(i)} for i in range(len(split_text))]
        )

        qa_chain = load_qa_with_sources_chain(
            ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",), chain_type="map_rerank"
        )

        qa = RetrievalQAWithSourcesChain(
            combine_documents_chain=qa_chain,
            retriever=docsearch.as_retriever(),
            reduce_k_below_max_tokens=True,
        )

        res = qa({"question": _input}, return_only_outputs=True)

        return res['answer']
    except Exception as e:
        print(e)
        traceback.print_exc()
        return ""


# def truncate_text(text, max_tokens):
#     tokens = text.split()
#     truncated_tokens = tokens[:max_tokens]
#     truncated_text = " ".join(truncated_tokens)
#     return truncated_text
#
#
# async def gpt_info_via_text(text, question):
#     template = """You are a very good analyst of startups. Answer task below based on context information below. Don't try to make up answer. If you're not sure about the answer, just write "I don't know."
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
#     context = truncate_text(text, 2048)
#
#     res = await llm_chain.arun({'question': question, 'context': context})
#
#     print(res)
#     return res


# async def gpt_info_via_text(text, question):
#     try:
#         output_parser = CommaSeparatedListOutputParser()
#         format_instructions = output_parser.get_format_instructions()
#
#         template = """You are a very good analyst of startups. Answer task below based on context information below. Don't try to make up answer. If you not sure about the answer just write "I don't know"
# Task: {question}
#
# Context:
# {context}
#
# Format output:
# {format_instructions}
#
# Your answer:
# """
#
#         prompt = PromptTemplate(
#             template=template,
#             input_variables=["question", "context"],
#             partial_variables={"format_instructions": format_instructions}
#         )
#
#         llm = ChatOpenAI(
#             temperature=0,
#             model_name="gpt-3.5-turbo",
#         )
#
#         llm_chain = LLMChain(prompt=prompt, llm=llm)
#
#         question = question
#         context = text
#
#         res = await llm_chain.arun({'question': question, 'context': context})
#
#         print(res)
#         return res
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#         return ""
