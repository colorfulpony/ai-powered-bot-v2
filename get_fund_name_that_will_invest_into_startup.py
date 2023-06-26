import os

import openai
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

from prompts import TEST_PROMPT5


# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Access the API key and use it in API requests
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

def get_fund_name_that_will_invest_into_startup(query, data):
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
    _input = TEST_PROMPT5.format_prompt(subject=query)
    answer = chain.run(input_documents=docs, question=_input)

    # if answer.lower().startswith("yes"):
    #     return data["vc_name"]
    # else:
    #     print(f"{data['vc_name']} will not invest into user startup")
    #     return "No"
    return answer