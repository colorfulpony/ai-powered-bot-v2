import traceback

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
            ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",), chain_type="stuff"
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