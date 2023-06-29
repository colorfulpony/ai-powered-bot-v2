from langchain import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser, StructuredOutputParser
from response_schemas import LAST_RESPONSE_RESPONSE_SCHEMA, LAST_RESPONSE_WITH_STARTUPS_NAMES_RESPONSE_SCHEMA, \
    LAST_RESPONSE_INDIVIDUAL_EMAIL

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
    template="You have been given information about an investment fund. Your task is to analyze the information and find or assume what {subject} of startups this fund is investing in or has already invested in.\n Here is a list of all possible stages: Idea Stage, Pre-Seed Stage, Seed Stage, Series A Stage, Series B Stage, Series C Stage, Series D Stage, Series E Stage, Late Stage, IPO Stage.\n If you are not sure of the answer, just write 'I don't know'. \n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)
STAGES_INPUT = INDUSTRIES_PROMPT.format(subject="stages")

# test
TEST_PROMPT = PromptTemplate(
    template="""You got information form a CSV File that has information about a lot of Venture Capital Funds. FOR YOUR ANSWER YOU ONLY THIS INFORMATION
 
TASK:
Your task is to find Venture Capital Funds that are most likely to invest in described below startup. 
In response, write a list of the Venture Capital Funds names that probably will invest in startup described below.
If a startup from a venture capital fund's investment portfolio solves the same or similar user problem as the startup described below, this fund will probably invest in the startup described below. 

For your answer you must find at least 10 funds

Don't make up fake information for your answer
Don't use any other venture capital funds other than the funds given to you before.

INFORMATION ABOUT STARTUP:
{subject}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

YOUR ANSWER:
""",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)
TEST_INPUT = TEST_PROMPT.format(subject="stages")

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



# test
MATCHED_VC_NAMES_PROMPT_v5 = PromptTemplate(
    template="""
------
INFORMATION ABOUT VENTURE CAPITALS:
------
{context}
------

------
GENERAL DESCRIPTION:
------
You got information about a lot of different venture capitals
------

------
YOUR TASK:
------
Based only on the information you have recently received, find the funds/companies/firms that are likely to invest in the startup described below. 
------

------
IMPORTANT THINGS:
------
First column with name `vc_name` in context is the column of names of venture capitals. Your answer must consist only of the names of the venture capitals in this column

If a startup from a venture capital's investment portfolio has similar description or works in similar industry as the startup described below, this fund will probably invest in the startup. 

In response, you must write a list of the names of these venture capitals separated by commas. 

Find minimum 5 venture capital funds that will invest in startup described below

Don't make up information.
Use only the information that you were given before for your answer.
------

------
STARTUP DESCRIPTION:
------
{question}
------

------
OUTPUT FORMAT INSTRUCTIONS:
------
{format_instructions}
------
""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": format_instructions}
)


# test
MATCHED_VC_NAMES_PROMPT_v6 = PromptTemplate(
    template="""Context information\n
{context}\n

Given the context information and not prior knowledge, do task described in details below:\n
{question}\n{format_instructions}""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": format_instructions}
)





last_response_output_parser = StructuredOutputParser.from_response_schemas(LAST_RESPONSE_RESPONSE_SCHEMA)
last_response_format_instructions = last_response_output_parser.get_format_instructions()

last_response_with_startups_names_output_parser = StructuredOutputParser.from_response_schemas(LAST_RESPONSE_WITH_STARTUPS_NAMES_RESPONSE_SCHEMA)
last_response_with_startups_names_format_instructions = last_response_with_startups_names_output_parser.get_format_instructions()

last_response_individual_email_output_parser = StructuredOutputParser.from_response_schemas(LAST_RESPONSE_INDIVIDUAL_EMAIL)
last_response_individual_email_format_instructions = last_response_individual_email_output_parser.get_format_instructions()

# last response

LAST_ANSWER_PROMPT = PromptTemplate(
    template="""Base your answer on the USER'S STARTUP INFORMATION and CONTEXT
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

LAST_ANSWER_WITH_STARTUPS_NAMES_PROMPT = PromptTemplate(
    template="""Below you got information about user's startup and information about investment fund.
Based on provided below information, write answer based on the OUTPUT FORMAT INSTRUCTIONS
All data in your response should be only from the information provided below. Don't make up any data. 

{question}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

If you think that there is no needed information for answer - just write "I don't know"

CONTEXT:
{context}
""",
    input_variables=["question", "context"],
    partial_variables={"format_instructions": last_response_individual_email_format_instructions}
)





# REFINE PROMPTS

DEFAULT_REFINE_PROMPT_TMPL_V1 = """You got next part of information from a CSV File that has information about a lot of Venture Capital Funds. FOR YOUR ANSWER YOU  MUST USE ONLY THIS INFORMATION
---------------------\n
{context_str}\n
---------------------\n

IMPORTANT TO KNOW:
We have provided an existing answer, including sources: {existing_answer}\n
We have the opportunity to refine the existing answer (only if needed) with some more context abowe.\n

TASK:
Your task is to find Venture Capital Funds that are most likely to invest in described below startup. 
In response, write a list of the Venture Capital Funds names that probably will invest in startup described below. Write as much matched funds as you can find.

Complete the previous answer with the new names of the funds. For example: 
If answer was: 
asd, qwe
How answer should looks like after improvement :
asd, qwe, zxc, xyz 

Don't make up fake information for your answer
Don't use any other venture capital funds other than the funds given to you before.

INFORMATION ABOUT STARTUP:
{question}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

YOUR ANSWER:"""

DEFAULT_REFINE_PROMPT_V1 = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=DEFAULT_REFINE_PROMPT_TMPL_V1,
    partial_variables={"format_instructions": format_instructions}
)

DEFAULT_TEXT_QA_PROMPT_TMPL_V1 = """You got part of information from a CSV File that has information about a lot of Venture Capital Funds. FOR YOUR ANSWER YOU ONLY THIS INFORMATION
---------------------\n
{context_str}\n
---------------------\n

TASK:
Your task is to find Venture Capital Funds that are most likely to invest in described below startup. 
In response, write a list of the Venture Capital Funds names that probably will invest in startup described below. For your answer you must find at least 5 funds 

Don't make up fake information for your answer
Don't use any other venture capital funds other than the funds given to you before.

INFORMATION ABOUT STARTUP:
{question}

OUTPUT FORMAT INSTRUCTIONS:
{format_instructions}

YOUR ANSWER:
"""

DEFAULT_TEXT_QA_PROMPT_V1 = PromptTemplate(
    input_variables=["context_str", "question"],
    template=DEFAULT_TEXT_QA_PROMPT_TMPL_V1,
    partial_variables={"format_instructions": format_instructions}
)








DEFAULT_REFINE_PROMPT_TMPL_V2 = """
------
GENERAL DESCRIPTION:
------
We have a list of venture capital funds: `{existing_answer}` that are likely to invest in the startup described below. 
Now you have the opportunity to expand this list (if possible) with the help of new venture funds, information about which you have in CONTEXT
------

------
CONTEXT:
------  
{context_str}
------

------
YOUR TASK:
------
Find the venture capital funds that are likely to invest in the startup described below (if possible from the new context above). 
Add to the list of funds I gave you earlier all the funds that you think are likely to invest in the startup described below
------

------
INFORMATION THAT IS IMPORTANT TO KNOW:
------
If a startup from a venture capital fund's portfolio solves the same or similar user problem as the startup described below, this fund will probably invest in the startup described below. 

If there are no funds that are likely to invest in the startup described below with the new context, you must return the answer as it is now

Don't make up information

Use only information from the context above to EXPAND existing answer

In response, EXPAND the existing list of funds with the names of the new funds separated by commas.
------

------
STARTUP DESCRIPTION:
------
{question}
------

------
OUTPUT FORMAT INSTRUCTIONS:
------
If you find new fund(s) from a new context that may invest in the described startup, you must add new funds to the existing list of fund that you got at the biginning, separated by commas. 

eg:
If the existing list is: `foo, bar, baz`.
And you found that `xyz` and `abc` funds is probably will invest in the described above startup.
Then your updated list should be: `foo, bar, baz, xyz, abc`

If you don't find any new funds, you must return list of fund that you got at the beginning
------
"""


DEFAULT_REFINE_PROMPT_V2 = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=DEFAULT_REFINE_PROMPT_TMPL_V2,
)

DEFAULT_TEXT_QA_PROMPT_TMPL_V2 = """
------
GENERAL DESCRIPTION:
------
You got context information below.
This information is a part of a large CSV file about a large number of different  venture capital funds.
------

------
CONTEXT:
------  
{context_str}
------

------
YOUR TASK:
------
Find the funds from the context above that are likely to invest in the startup described below. 
Find as much funds as you can
------

------
INFORMATION THAT IS IMPORTANT TO KNOW:
------
If a startup from a venture capital fund's investment portfolio solves the same or similar problem as the startup described below, this fund will probably invest in the startup described below. 

In response, write a list of the names of these venture capital funds separated by commas and nothing else. Find as many funds as possible.

Don't make up information
Use only the information in the context above for your answer.
------

------
STARTUP DESCRIPTION:
------
{question}
------

------
OUTPUT FORMAT INSTRUCTIONS:
------
{format_instructions}
------
"""

DEFAULT_TEXT_QA_PROMPT_V2 = PromptTemplate(
    input_variables=["context_str", "question"],
    template=DEFAULT_TEXT_QA_PROMPT_TMPL_V2,
    partial_variables={"format_instructions": format_instructions}
)








DEFAULT_REFINE_PROMPT_TMPL_V3 = ("The startup description is as follows: {question}\n"
    "We have provided an existing list if venture capital funds," 
    "that are likely to invest in startup described above, including sources: {existing_answer}\n"
    "We have the opportunity to refine the existing answer"
    "(only if needed) with some more context about new funds below.\n"
    "------------\n"
    "{context_str}\n"
    "------------\n"
    "Given the new context, refine the original answer to find more funds"
    "that are likely to invest in described above startup. "
    "If you find new fund(s) from a new context that may invest in the described startup, "
    "you must return the old list of funds + the list of new funds separated by commas and NOTHING ELSE." 
    "eg:"
    "The existing list: `foo, bar, baz`."
    "Updated list: `foo, bar, baz, xyz"
    "If you don't find any new funds, you must just return the old answer and NOTHING ELSE"
    "Do not write any comments, just the list of funds."
    "If you do update list, please update the sources as well. "
)

DEFAULT_REFINE_PROMPT_V3 = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=DEFAULT_REFINE_PROMPT_TMPL_V3,
)

DEFAULT_TEXT_QA_PROMPT_TMPL_V3 = (
    "Context information about venture capital funds is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given the context information and not prior knowledge, "
    "find venture capital funds that are likely to invest in this startup: {question}\n"
    "{format_instructions}"
)

DEFAULT_TEXT_QA_PROMPT_V3 = PromptTemplate(
    input_variables=["context_str", "question"],
    template=DEFAULT_TEXT_QA_PROMPT_TMPL_V3,
    partial_variables={"format_instructions": format_instructions}
)

DEFAULT_REFINE_PROMPT_TMPL_V4 = """
`{context_str}
{question}`


IF YOU UNDERSTAND THIS MESSAGE YOU MUST RETURN `{existing_answer}` AND NOTHING ELSE:
"""

DEFAULT_REFINE_PROMPT_V4 = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=DEFAULT_REFINE_PROMPT_TMPL_V4,
)

DEFAULT_TEXT_QA_PROMPT_TMPL_V4 = """
------
CONTEXT:
------  
{context_str}
------

Answer question below using only context above.

------
QUESTION:
------
{question}
------
"""

DEFAULT_TEXT_QA_PROMPT_V4 = PromptTemplate(
    input_variables=["context_str", "question"],
    template=DEFAULT_TEXT_QA_PROMPT_TMPL_V4,
)








DEFAULT_REFINE_PROMPT_TMPL_V5 = """
------
GENERAL DESCRIPTION:
------
We have a list of venture capital funds: `{existing_answer}` that are likely to invest in the startup described below. 
Now you have the opportunity to expand this list (if possible) with the help of new venture funds, information about which you have in CONTEXT
------

------
CONTEXT:
------  
{context_str}
------

------
YOUR TASK:
------
Find the venture capital funds that are likely to invest in the startup described below (if possible from the new context above). 
------

------
INFORMATION THAT IS IMPORTANT TO KNOW:
------
If a startup from a venture capital fund's portfolio solves the same or similar user problem as the startup described below, this fund will probably invest in the startup described below. 

If there are no funds that are likely to invest in the startup described below with the new context, you must return the answer as it is now

Don't make up information

Use only information from the context above to EXPAND existing answer

In response, EXPAND the existing list of funds with the names of the new funds separated by commas.
------

------
STARTUP DESCRIPTION:
------
{question}
------

------
OUTPUT FORMAT INSTRUCTIONS:
------
If you find new fund(s) from a new context that may invest in the described startup, you must add new funds to the existing answer separated by commas and NOTHING ELSE. 

eg:
If the existing list was: `foo, bar, baz`.
And you found that `xyz` fund is probably will invest in the described above startup.
Then your updated list must be: `foo, bar, baz, xyz

If you don't find any new funds, you should just return the EXISTING ANSWER and NOTHING ELSE
------
"""


DEFAULT_REFINE_PROMPT_V5 = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=DEFAULT_REFINE_PROMPT_TMPL_V5,
)

DEFAULT_TEXT_QA_PROMPT_TMPL_V5 = """
------
GENERAL DESCRIPTION:
------
You got context information below.
This information is a part of a large CSV file about a large number of different  venture capital funds.
------

------
CONTEXT:
------  
{context_str}
------

------
YOUR TASK:
------
Find the funds from the context above that are likely to invest in the startup described below. 
------

------
INFORMATION THAT IS IMPORTANT TO KNOW:
------
If a startup from a venture capital fund's investment portfolio solves the same or similar problem as the startup described below, this fund will probably invest in the startup described below. 

In response, write a list of the names of these venture capital funds separated by commas and nothing else. Find as many funds as possible.

Don't make up information
Use only the information in the context above for your answer.
------

------
STARTUP DESCRIPTION:
------
{question}
------

------
OUTPUT FORMAT INSTRUCTIONS:
------
{format_instructions}
------
"""

DEFAULT_TEXT_QA_PROMPT_V5 = PromptTemplate(
    input_variables=["context_str", "question"],
    template=DEFAULT_TEXT_QA_PROMPT_TMPL_V5,
    partial_variables={"format_instructions": format_instructions}
)











DEFAULT_REFINE_PROMPT_TMPL_V6 = """
We created an existing list of venture capital funds `{existing_answer}` that probably will invest in this startup: {question}\n

Now we have the opportunity to increase the existing list with some more venture capital funds because we got new funds below.\n
------------\n
{context_str}\n
------------\n

------
How to determine whether a fund will invest in a startup?
------
If venture capital fund has invested in startup(s) that works in a similar industry to the startup described above, then the fund will invest in the startup described above.
Therefore, you can add name of this fund to the existing list of funds.
------

Find as much matched funds as you can

If you do update existing list, please just add new funds, don't remove previous.
If new venture capital funds isn't useful, you must return the existing list of venture capital funds and nothing else.

{format_instructions}
"""

DEFAULT_REFINE_PROMPT_V6 = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=DEFAULT_REFINE_PROMPT_TMPL_V6,
    partial_variables={"format_instructions": format_instructions}
)


DEFAULT_TEXT_QA_PROMPT_TMPL_V6 = """Information about venture capital funds is below.
\n---------------------\n
{context_str}
\n---------------------\n

Given the context information and not prior knowledge, find venture capital funds that probably will invest in this startup:
{question}\n

------
How to determine whether a fund will invest in a startup?
------
If venture capital fund has invested in startup(s) that works in a similar industry to the startup described below, then the fund will invest in the startup described below.
Therefore, you can add name of this fund to your answer.
------

Find as much matched funds as you can

{format_instructions}"""

DEFAULT_TEXT_QA_PROMPT_V6 = PromptTemplate(
    input_variables=["context_str", "question"],
    template=DEFAULT_TEXT_QA_PROMPT_TMPL_V6,
    partial_variables={"format_instructions": format_instructions}
)






DEFAULT_REFINE_PROMPT_TMPL_V7 = """Existing List of Venture Capital Funds: {existing_answer}.
This is a list of names of Venture Capital Funds that are likely to invest in the following startup:

Startup Description:
{question}

We have new venture capital funds available to expand the existing list:

New Venture Capital Funds:
{context_str}

To determine whether a fund will invest in a startup, use the following criteria:
- If a venture capital fund has previously invested in startups operating in a similar industry(`vc_portfolio_startup_solution`) as the described startup, it is likely to invest in the described startup.
- Add the name of any fund that matches the criteria to the existing list of funds.

For your answer, use only the names of venture capital funds from the context(`vc_name`)

There should be at least 5 funds in total.

If you find any new funds that meet the criteria, concatenate them with the existing list. If no new funds match the criteria, return the existing list without any changes.

Please update the existing list by concatenating it with any additional venture capital funds that match the given criteria."""

DEFAULT_REFINE_PROMPT_V7 = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=DEFAULT_REFINE_PROMPT_TMPL_V7,
)


DEFAULT_TEXT_QA_PROMPT_TMPL_V7 = """Context:
{context_str}

Given the provided context, find venture capital funds that are likely to invest in the following startup:

Startup Description:
{question}

To determine whether a fund will invest in a startup, consider the following criteria:
- If a venture capital fund has previously invested in startups operating in a similar industry(`vc_portfolio_startup_solution`) as the described startup, it is likely to invest in the described startup.
- Include the name of the fund in your answer if it matches the criteria.

There should be at least 5 funds in total.

For your answer, use only the names of venture capital funds from the context(`vc_name`)

Please provide a list of venture capital funds that match the given criteria.

Response format:
{format_instructions}
"""

DEFAULT_TEXT_QA_PROMPT_V7 = PromptTemplate(
    input_variables=["context_str", "question"],
    template=DEFAULT_TEXT_QA_PROMPT_TMPL_V7,
    partial_variables={"format_instructions": format_instructions}
)







# test
TEST_PROMPT2 = PromptTemplate(
    template="""
------
GENERAL DESCRIPTION:
------
You got information about a lot of different venture capitals
------

------
YOUR TASK:
------
Based only on the information you have recently received, find the funds/companies/firms that are likely to invest in the startup described below. 
------

------
IMPORTANT THINGS:
------
If a startup from a venture capital's investment portfolio has similar description or works in similar industry as the startup described below, this fund will probably invest in the startup. 

In response, you must write a list of the names of these venture capitals separated by commas. 

Find minimum 5 venture capitals

Don't make up information.
Use only the information that you were given before for your answer.
------

------
STARTUP DESCRIPTION:
------
{subject}
------

------
OUTPUT FORMAT INSTRUCTIONS:
------
{format_instructions}
------
""",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)


TEST_PROMPT3 = PromptTemplate(
    template="""
------
YOUR TASK:
------
Find 5 venture capital funds that are likely to invest in the startup described below.
------

------
STARTUP DESCRIPTION:
------
{subject}
------

------
How to determine whether a fund will invest in a startup?
------
If venture capital fund has invested in startup(s) that works in a similar industry or solve similar problem(this info you can find in `vc_portfolio_startup_solution`) to the industry in which startup described above works, then the fund will invest in the startup described above.
Therefore, you can add name of this fund to your answer.
------

------
Important notes:
------
Do not make up venture capital fund names
Use only venture capital fund names from the context you were given before
Names of funds you can find only in the context called `vc_name`
Don't write fictitious fund names. If you can't find 5 funds, then after all the funds you found, just write "That's it"
------

------
Output format:
------
{format_instructions}
------
""",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)





TEST_PROMPT4 = PromptTemplate(
    template="""
------
YOUR TASK:
------
Understand whether a venture fund will invest in the startup described below or not
------

------
STARTUP DESCRIPTION:
------
{subject}
------

------
How to determine whether a fund will invest in a startup?
------
If venture capital fund has invested in startup(s) that works in a similar industry or solve similar problem to the industry in which startup described above works, then the fund will invest in the startup described above.(you can find startup in wich fund has invested in `vc_portfolio`.
Therefore, you can think of this fund as one that will invest in a startup described above. In this case, you only need to write the name of this fund and nothing else!

If this fund has not invested in startup(s) that works in a similar industry or has not solve similar problem to the industry in which startup described above works, it will not invest in the startup. In this case, you need simply write "This fund is not suitable"
------
""",
    input_variables=["subject"],
    validate_template=False
)





CHECK_IF_FUND_WILL_INVEST_IN_USER_STARTUP_PROMPT = PromptTemplate(
    template="""
Find out whether the fund (information about which you got from context) will invest in the startup described below or not. 
To answer, use only the data that was provided to you earlier, and not any other data

------
How to determine whether a fund will invest in a startup?
------
If the venture capital fund has invested in a startup(s) that operates in a similar industry or solves similar problems to the startup described below, then the fund will invest in the startup (you can find the startup in which the fund has invested in the `vc_portfolio`).
------

If you think that the fund has in its investment portfolio startup(s) that operate in a similar industry or solve a similar problem to the startup described below, YOU MUST ANSWER `Yes`.
In any other way, please return just "No"

------
Startup Description:
------
{subject}
------
""",
    input_variables=["subject"],
    validate_template=False
)
