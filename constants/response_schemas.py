from langchain.output_parsers import ResponseSchema

LAST_RESPONSE_INDIVIDUAL_EMAIL = [
    ResponseSchema(
        name="Individual email message",
        description="""Write a paragraph that can be inserted into the analyst's email, the purpose of which is to show that the investor has invested in a company that is similar to the user's startup. Therefore, write the paragraph as follows: "I noticed that you have invested in [insert name and website address of 1(maximum 2) startup from the VC investment portfolio that solves problem of similar industry as the user's startup] that are focused on [insert problems these startups are solving], seeing that, I think we could be a great fit because we are [insert problem the user's startup is solving]."""
    )
]
