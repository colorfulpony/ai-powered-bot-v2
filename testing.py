import os
import traceback

import openai
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from get_info_about_fund import get_info_about_fund
from prompts import TEST_PROMPT, DEFAULT_TEXT_QA_PROMPT_V2, DEFAULT_REFINE_PROMPT_V2, TEST_PROMPT2
from refactor_output import refactor_output


# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Access the API key and use it in API requests
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key




def get_matched_fund_names(query):
    try:
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma(persist_directory="chroma_save", embedding_function=embeddings)

        # loader = CSVLoader(file_path='csvs/new_data.csv', encoding="utf-8", csv_args={
        #     'delimiter': ',',
        #     'fieldnames': [
        #         'vc_name', 'vc_website_url', 'vc_linkedin_url', 'vc_investor_name',
        #         'vc_investor_email', 'vc_stages', 'vc_industries',
        #         'vc_portfolio_startup_name', 'vc_portfolio_startup_website_url',
        #         'vc_portfolio_startup_solution'
        #     ]
        # })
        #
        # documents = loader.load()
        #
        # text_splitter = CharacterTextSplitter(chunk_size=20000, chunk_overlap=0)
        # docs = text_splitter.split_documents(documents)
        #
        # embeddings = OpenAIEmbeddings()
        # docsearch = Chroma.from_documents(
        #     documents=docs,
        #     embedding=embeddings,
        # )

        qa_chain = load_qa_chain(
            ChatOpenAI(
                temperature=0,
                model_name="gpt-3.5-turbo-16k",
            ),
            chain_type="refine",
            question_prompt=DEFAULT_TEXT_QA_PROMPT_V2,
            refine_prompt=DEFAULT_REFINE_PROMPT_V2
        )

        qa = RetrievalQA(
            combine_documents_chain=qa_chain,
            retriever=docsearch.as_retriever(),
        )

        _input = TEST_PROMPT2.format(subject=query)
        res = qa(
            {"query": query},
            return_only_outputs=True
        )

        print(res['result'])
        return res['result']
    except Exception as e:
        print(e)
        traceback.print_exc()
        return ""


def main():
    print("Bot is ready to chat. Type 'exit' to stop chatting.")

    # startup_name = input("Enter the startup name: ")
    # startup_industry = input("Enter the startup industry: ")
    # startup_stage = input("Enter the startup stage: ")
    # problems_solved = input("Enter the problems solved by the startup: ")

    # startup_name = "Debonne"
    # startup_industry = "Healthcare"
    # startup_stage = "Seed"
    # problems_solved = "It produces pills for third party countries"

    # startup_name = "Juko"
    # startup_industry = "Finance, automation, money"
    # startup_stage = "Seed, early-stage, and Series A"
    # problems_solved = "It solves the user problem of automating key areas of business operations such as invoicing, payment collections, bulk payouts, GST filing, and customer data management."

    startup_name = "SIRPLUS"
    startup_industry = "B2C, Ecommerce, Climate Tech"
    startup_stage = "Seed"
    problems_solved = "It helps consumer to buy let over food from store at an attractive price to help reduce foodwaste and save the planet"

    query = f"{startup_name} is a startup that works at {startup_stage} stage(s) in the {startup_industry} industry(s) that solves the following problems: {problems_solved}."
    funds = get_matched_fund_names(query)

    # if funds.startswith("Sorry, try again"):
    #     print(funds)
    # else:
    #     fund_names = funds.split(", ")
    #     for fund_name in fund_names:
    #         if fund_name.startswith("these are all the funds that are likely to invest in the startup"):
    #             print(fund_name)
    #         else:
    #             raw_info = get_info_about_fund(fund_name, query)
    #             info = refactor_output(raw_info)
    #
    #             print(info)


if __name__ == '__main__':
    main()
