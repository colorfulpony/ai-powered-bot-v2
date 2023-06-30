import traceback

from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI


async def gpt_info_via_text(text, question):
    """
    Get answer from LLM based on text and input about startup from vc's portfolio

    Parameters:
        text (str): Text-information about portfolio's startup
        _input (str): Question to ask LLM

    Returns:
        str: Answer to question from LLM
    """
    try:
        # Define the template for the prompt
        template = """You are a very good analyst of startups. Answer task below based on context information below. Don't try to make up answer.
        Task: {question}

        Context:
        {context}

        Your answer:
        """

        # Create a prompt template with the defined template and input variables
        prompt = PromptTemplate(template=template, input_variables=["question", "context"])

        # Create a ChatOpenAI language model
        llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo-16k",
        )

        # Create an LLMChain with the prompt template and language model
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        # Set the question and context for the prompt
        question = question
        context = text

        # Generate a response using the LLMChain
        res = await llm_chain.arun({'question': question, 'context': context})

        return res
    except Exception as e:
        print(e)
        traceback.print_exc()
        return ""


if __name__ == '__main__':
    # Example usage
    test = gpt_info_via_text()
