import traceback

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma


async def gpt_info_via_text(cleaned_text, _input):
    """
    Get answer from LLM based on text and input

    Parameters:
        cleaned_text (str): Text with context on which LLM must give answer
        _input (str): Question to ask LLM

    Returns:
        str: Answer to question from LLM
    """
    try:
        # Split the cleaned text into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', ' ', '.', ',', ''], chunk_size=500, chunk_overlap=80
        )
        split_text = text_splitter.split_text(cleaned_text)

        # Create OpenAI embeddings
        embeddings = OpenAIEmbeddings()

        # Create a Chroma vector store from the split text
        docsearch = Chroma.from_texts(
            split_text, embeddings, metadatas=[{"source": str(i)} for i in range(len(split_text))]
        )

        # Load the question-answering chain
        qa_chain = load_qa_with_sources_chain(
            ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",), chain_type="stuff"
        )

        # Create a retrieval-based QA chain
        qa = RetrievalQAWithSourcesChain(
            combine_documents_chain=qa_chain,
            retriever=docsearch.as_retriever(),
            reduce_k_below_max_tokens=True,
        )

        # Perform the question-answering task
        res = qa({"question": _input}, return_only_outputs=True)

        return res['answer']
    except Exception as e:
        print(e)
        traceback.print_exc()
        return ""
