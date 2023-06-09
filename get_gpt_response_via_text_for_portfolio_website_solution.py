import traceback

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI


async def gpt_info_via_text(text, question):
    try:
        template = """You are a very good analyst of startups. Answer task below based on context information below. Don't try to make up answer. If you not sure about the answer just write "I don't know"
    Task: {question}
    
    Context:
    {context}
    
    Your answer:
    """

        prompt = PromptTemplate(template=template, input_variables=["question", "context"])

        llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-3.5-turbo",
            )

        llm_chain = LLMChain(prompt=prompt, llm=llm)

        question = question
        context = text

        res = await llm_chain.arun({'question': question, 'context': context})

        return res
    except Exception as e:
        print(e)
        traceback.print_exc()
        return ""

