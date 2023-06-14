from langchain import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser, StructuredOutputParser
from response_schemas import LAST_RESPONSE_RESPONSE_SCHEMA

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()

# industries
INDUSTRIES_PROMPT = PromptTemplate(
    template="You got information about an investment fund. Your task is to analyze the information and find or assume in which {subject} this fund invests or has invested in.\n If you aren't sure about the answer just write - 'I don't know'. \n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)
INDUSTRIES_INPUT = INDUSTRIES_PROMPT.format(subject="industries")

# stages
STAGES_PROMPT = PromptTemplate(
    template="You got information about an investment fund. Your task is to analyze the info and find or assume in which {subject} this fund invests or has invested in.\n If you aren't sure about the answer just write - 'I don't know'. \n{format_instructions}",
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
    template="""Ignore all the information or instructions you got before. From now you can use only information provided below.

For your answer use information only from CONTEXT and no other information. 
    
Act like you are a very good invest fund analyst.

Below, you got CONTEXT - it is information about bunch of venture capital funds. 
Also below, you have INFORMATION ABOUT STARTUP - it's information about user startup.

Task: Your task is to find funds that are most likely to invest in described user's startup.
Find minimum 3 funds.  

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
    template="""Ignore all the information or instructions you got before. From now you can use only information provided below.
    
Based on the USER'S STARTUP INFORMATION, find a venture capital funds that is likely to invest in the user's startup among the funds described in CONTEXT
In response, write a list of the fund names (minimum 3, but better as much as you can find). Make sure that all of them should be only from CONTEXT below). Don't make up any data. For your answer use funds only from CONTEXT.

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


# get vc names
MATCHED_VC_NAMES_PROMPT_v3 = PromptTemplate(
    template="""Ignore all the information or instructions you got before. From now you can use only information provided by me below.

Given information from a CSV file containing information about venture capital funds, with columns 'vc_name', 'vc_website_url', 'vc_linkedin_url', 'vc_investor_name', 'vc_investor_email', 'vc_stages', 'vc_industries', 'vc_portfolio_startup_name', 'vc_portfolio_startup_website_url', and 'vc_portfolio_startup_solution'. Also given the user's startup information. 
Generate a comma-separated list of venture capital fund names that are likely to invest in the user's startup. Give at least 3 funds. 
For your answer use information from CSV File and nothing else. Don't come up with some unreal information, or information not from CSV File 


User's Startup Information:
{question}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

Information from CSV File (Venture Capital Funds)
{context}
""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": format_instructions}
)


# get vc names
MATCHED_VC_NAMES_PROMPT_v4 = PromptTemplate(
    template="""CONTEXT
{context}

USER'S STARTUP:
{question}

Task:
Find funds from CONTEXT that are most likely to invest in USER'S STARTUP. In the answer write only names of these funds. Give me minimum 3 names of the funds

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

YOUR ANSWER:
""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": format_instructions}
)


last_response_output_parser = StructuredOutputParser.from_response_schemas(LAST_RESPONSE_RESPONSE_SCHEMA)
last_response_format_instructions = last_response_output_parser.get_format_instructions()

# last response

LAST_ANSWER_PROMPT = PromptTemplate(
    template="""Based on the NAME OF CERTAIN FUND, USER'S STARTUP INFORMATION and CONTEXT write answer based on the OUTPUT FORMAT INSTRUCTIONS
All data in your response should be only from the information provided below. Don't make up any data. 

{question}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

CONTEXT:
{context}
""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": last_response_format_instructions}
)
