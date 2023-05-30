from langchain import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser, StructuredOutputParser
from response_schemas import LAST_RESPONSE_RESPONSE_SCHEMA

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

# industries
INDUSTRIES_PROMPT = PromptTemplate(
    template="You got information about an investment fund. Your task is to analyze the info and find or assume in which {subject} this fund invests or has invested in. If you don't know the answer just write 'I don't know'. \n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)
INDUSTRIES_INPUT = INDUSTRIES_PROMPT.format(subject="industries")

# stages
STAGES_PROMPT = PromptTemplate(
    template="You got information about an investment fund. Your task is to analyze the info and find or assume in which {subject} this fund invests or has invested in. If you don't know the answer just write 'I don't know'. \n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)
STAGES_INPUT = INDUSTRIES_PROMPT.format(subject="stages")

# solution
SOLUTION_PROMPT = PromptTemplate(
    template="""You are a very good analyst of startups.
Task: You got information about an startup. Your task is to find out what are the users {subject} that this startup solves. Describe it briefly, clearly and simply. 5 sentences.

Example of desired answer format:
Startup aims to solve the problem of maintaining a healthy and beautiful garden for people who lack the time, knowledge, or resources to do it themselves. It provide a subscription-based service that offers regular visits from their trained gardeners who take care of all the necessary tasks such as watering, fertilizing, pruning, and pest control. They also use eco-friendly and sustainable practices to ensure a safe and healthy environment for both the plants and the customers. Their goal is to make gardening effortless and enjoyable for everyone, regardless of their experience level or busy schedules.""",
    input_variables=["subject"]
)
SOLUTION_INPUT = INDUSTRIES_PROMPT.format(subject="problems")


# get vc names
MATCHED_VC_NAMES_PROMPT = PromptTemplate(
    template="""To answer this question, use only CONTEXT and no other information. 
    
You are a very good invest fund analyst. At the very end of this message, you got CONTEXT - information about venture capital funds. Also, you have INFORMATION ABOUT STARTUP - it's information about user startup.
Task: Your task is to find funds that are most likely to invest in described startup below. In you answer write comma-separated lidst of venture capital funds. Find at least 5 funds(Better find as much matched ventures as you can). But use only venture capital funds from CONTEXT.

Here are 2 criteria by which you can understand whether a fund will invest in a startup:
1) Fund's portfolio should include startup(s) that offer similar problem solution to the problem solution of the startup described below. 
2) The industries in which the fund invests should be similar to the industry in which the startup described below works 

Don't make up fake information for your answer
Don't use any other venture capital funds other than the funds given to you in CONTEXT
Always give list of fund names

INFORMATION ABOUT STARTUP:
{question}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

CONTEXT:
{context}
""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": format_instructions}
)

# get vc names
MATCHED_VC_NAMES_PROMPT_v2 = PromptTemplate(
    template="""Based on the USER'S STARTUP INFORMATION, find a venture capital funds that is likely to invest in the user's startup among the funds described in CONTEXT
In response, write a list of the names of these funds separated by commas(at least 3 funds, but all of them should be from CONTENXT)

USER'S STARTUP INFORMATION:
{question}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

CONTEXT:
{context}
""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": format_instructions}
)



last_response_output_parser = StructuredOutputParser.from_response_schemas(LAST_RESPONSE_RESPONSE_SCHEMA)
last_response_format_instructions = last_response_output_parser.get_format_instructions()

# last response
LAST_ANSWER_PROMPT = PromptTemplate(
    template="""INFORMATION ABOUT VENTURE FUNDS:
{context}
    
Use only the information provided above to do the task
    
You are a very good linkedin connection engineer. At the very beginning of this message, you got INFORMATION ABOUT VENTURE FUNDS.
Task: Your task is to give answer based on the OUTPUT FORMAT INSTRUCTIONS. 

DON'T MAKE UP ANY INFORMATION and FOR YOU ANSWER USE INFORMATION ONLY THAT I GAVE YOU
Your answer format should be only in OUTPUT FORMAT INSTRUCTIONS provided below

{question}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}
""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": last_response_format_instructions}
)
