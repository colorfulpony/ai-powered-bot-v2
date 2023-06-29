import os

import openai
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

from prompts import CHECK_IF_FUND_WILL_INVEST_IN_USER_STARTUP_PROMPT


# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Access the API key and use it in API requests
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

def check_if_fund_will_invest_in_user_startup(query, data):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0.0)

    data_str = ""
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                data_str += f"{key}: {item}\n"
        else:
            data_str += f"{key}: {value}\n"

    # Create a Document object
    doc = Document(page_content=data_str)

    # Use the document with load_qa_chain
    docs = [doc]

    # Load a question-answering chain with chain_type set to "stuff"
    chain = load_qa_chain(llm, chain_type="stuff")

    # Run the chain with the list of documents and your question
    _input = CHECK_IF_FUND_WILL_INVEST_IN_USER_STARTUP_PROMPT.format_prompt(subject=query)
    answer = chain.run(input_documents=docs, question=_input)

    return answer