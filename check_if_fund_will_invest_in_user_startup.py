import os
import traceback
from dotenv import load_dotenv
from pathlib import Path

import openai
from langchain import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings

from constants import prompts as INPUTS



# Access the API key and use it in API requests
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


def check_if_fund_will_invest_in_user_startup(information_about_user_startup, information_about_fund):
    """
    Check if a fund will invest in a user's startup based on provided information.

    Parameters:
        information_about_user_startup (str): Information about the user's startup.
        information_about_fund (dict): Information about the fund.

    Returns:
        str: The answer provided by the model if successful, or None if an error occurs.
    """
    try:
        # Convert the data into a string representation
        data_str = ""
        for key, value in information_about_fund.items():
            if isinstance(value, list):
                for item in value:
                    data_str += f"{key}: {item}\n"
            else:
                data_str += f"{key}: {value}\n"

        # Create a Document object
        doc = Document(page_content=data_str)

        # Use the document with load_qa_chain
        docs = [doc]

        # Create an embeddings object
        embeddings = OpenAIEmbeddings()

        # Create a document search object
        docsearch = FAISS.from_documents(docs, embeddings)

        # Create the question answering model
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0
        )

        # Create a retrieval-based question answering model
        qa = RetrievalQA.from_llm(llm=llm, retriever=docsearch.as_retriever(), prompt=INPUTS.CHECK_IF_FUND_WILL_INVEST_IN_USER_STARTUP_PROMPT)

        # Ask a question and get an answer
        answer = qa.run(query=information_about_user_startup)
        return answer
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None
