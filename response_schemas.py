from langchain.output_parsers import ResponseSchema

INDUSTRIES_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Industries in which the fund invests",
        description="""You are a very good analyst of investment companies. 
    Answer the task based on the context below. Keep the answer only in the format I have written below and not in any other format. Just write "-" and nothing else if you not sure about the answer or if there is no info about the industries at all. Don't ask questions. Don't write anything else. Don't write your explanations.
Task: Analyze the context given to you at the very end and find the industries in which this investment fund invests. Use only those industries that I wrote below."

Desired answer format:
<comma_separated_list_of_company_investing_industries>

Example of desired answer format:
AI, Biotech, Healthcare

Comma separated list of all investment industries: Technology, E-commerce, Healthcare, Finance, Education, Food, Beverage, Energy, Travel, Hospitality, Real Estate, Entertainment, Social Impact, Marketing, Advertising, Transportation, Logistics, Manufacturing, Agriculture, Fashion, Beauty, Personal Care, Fitness, Wellness, Home Services, Construction, Engineering, Automotive, Sports, Recreation, Art, Design, Media, Publishing, Government, Public Services, Professional Services, HR, Recruitment, Gaming, Esports, Insurance, Telecommunications, Security, Surveillance, Aerospace, Defense, Biotechnology, Pharmaceuticals, Chemicals, Consumer Electronics, Consumer Goods, Environmental Services, Hospitality, Events, Industrial Automation, Robotics, Legal Services, Materials Science, Medical Devices, Mining, Metals, Nanotechnology, Packaging, Containers, Plastics, Rubber, Retail, Social Media, Networking, Software, IT Services, Supply Chain, Logistics, Virtual, Augmented Reality, Crowdfunding, Fundraising, Internet of Things, Smart Homes, Robotics, Drones, AI, Machine Learning, Blockchain, Cryptocurrency, Quantum Computing, Space Exploration, Commercialization, Urban Farming, Agriculture, Waste Management, Recycling, Water, Waste Treatment, 3D Printing, Additive Manufacturing, Architecture, Design, Cloud Computing, Databases, Information Management, Design, User Experience, Digital Signage, Display Advertising,DTC Products, Distributed Ledger Technology, Document Management, Automation, Employee Benefits, Perks, Event Planning, Management, Facility Management, Maintenance, Financial Technology, Services, Fleet Management, Transportation Services, Food Delivery, Meal Kits, Health, Fitness Wearables, Home Security, Surveillance, Identity, Access Management, Influencer Marketing, Social Media Advertising, Intellectual Property Management, Internet Services, ISPs, Legal Tech, Services, Logistics, Supply Chain Management, Marketing Automation, Analytics, Medical Research, Development, Online Learning Platforms, MOOCs, Online Marketplaces, Auctions, Personalized Nutrition, Wellness, Privacy, Data Security, Procurement, Vendor Management, Product Design, Development, Professional Development, Training, Property Management, Maintenance, Public Relations, Communications, Renewable Energy, Clean Tech, Smart City, Infrastructure, Wearable Technology, IoT Devices, Advanced Materials, Agritech, Air Quality Control, Animal Health, Nutrition, App Development, Design, Asset Management, Investment, Audio, Music, Autonomous Vehicles, Behavioral Analytics, Insights, Big Data, Analytics, Bioinformatics, Genomics, Business Intelligence, Analytics, Cloud Services, Infrastructure, Cognitive Computing, AI, Collaborative Tools, Workspaces, Commercial Real Estate, Communication, Networking, Computer Vision, Image Processing, Construction Tech, Building Materials, Corporate Social Responsibility,CRM, Cybersecurity, Privacy, Data Science, Analysis, Defense, Security, Digital Currency, Payments, Digital Marketing, Advertising, Digital Rights Management, Disaster Response, Relief, Diversity, Equity,, Inclusion (DEI), Document Collaboration, Sharing, Drones, Unmanned Aerial Vehicles (UAVs), E-commerce Platforms, Marketplaces, Education Technology, Services, Electric Vehicles, Charging Infrastructure, Electronic Components, Devices, Emerging Technologies, Innovation, Employee Engagement, Retention, Energy Storage, Distribution, Enterprise Resource Planning (ERP), Environmental Monitoring, Assessment, Event Ticketing, Management, Facility Maintenance, Management, Fashion Technology, Wearables, Financial Planning, Management, Fleet Maintenance, Management, Food Science, Technology, Fraud Detection, Prevention, Gaming, Gamification, Geo-location Services, Analytics, Graphic Design, Animation."""
    )
]

STAGES_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Stages in which the fund invests",
        description="""You got information about an investment fund. Your task is to analyze the info and find out the investment stages in which this fund typically invests or has invested in the past.

        Output format:
        qwer, asdf, zxcv

        Your answer: """
    )
]

VC_PORTFOLIO_STARTUP_SOLUTION_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Solution of the startup",
        description="""You are a very good analyst of startups.
Task: You got information about an startup. Your task is to determine what user problem this startup solves Describe it briefly, clearly and simply. 5 sentences.

Example of desired answer format:
Startup aims to solve the problem of maintaining a healthy and beautiful garden for people who lack the time, knowledge, or resources to do it themselves. It provide a subscription-based service that offers regular visits from their trained gardeners who take care of all the necessary tasks such as watering, fertilizing, pruning, and pest control. They also use eco-friendly and sustainable practices to ensure a safe and healthy environment for both the plants and the customers. Their goal is to make gardening effortless and enjoyable for everyone, regardless of their experience level or busy schedules.

Your answer:
""")
]

LAST_RESPONSE_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Fund name",
        description="Write name of the investment fund"
    ),
    ResponseSchema(
        name="Fund website",
        description="Write the website url of the investment fund"
    ),
    ResponseSchema(
        name="Fund linkedIn",
        description="Write the linkedin url of the investment fund if there is such. If there is no linkedIn url - just write '/'"
    ),
    ResponseSchema(
        name="Analyst name",
        description="Write name of the analyst of the investment fund"
    ),
    ResponseSchema(
        name="Analyst email",
        description="Write email of the analyst of the investment fund"
    ),
    ResponseSchema(
        name="Individual email message",
        description="""A personalized email to an investment fund analyst. An email that can be used by the user to get investments from the fund where this analyst works."""
    )
]


LAST_RESPONSE_WITH_STARTUPS_NAMES_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Fund name",
        description="Write name of the investment fund"
    ),
    ResponseSchema(
        name="Fund website",
        description="Write the website url of the investment fund"
    ),
    ResponseSchema(
        name="Fund linkedIn",
        description="Write the linkedin url of the investment fund if there is such. If there is no linkedIn url - just write '/'"
    ),
    ResponseSchema(
        name="Analyst name",
        description="Write name of the analyst of the investment fund"
    ),
    ResponseSchema(
        name="Analyst email",
        description="Write email of the analyst of the investment fund"
    ),
    ResponseSchema(
        name="Individual email message",
        description="""Write a paragraph that can inserted to an email to the analyst, the objective of this paragraph is to show that the investor has invested in a company that are similar to the  user’s startup. Therefore, write paragraph as follow: “I notice that you have invested in [insert the name and website url of the first startup that solve very similar problems] and [insert the name and website url of the second  startup that solve very similar problems] which are focus on [Insert the problem they are solving], seeing this I think we could be a great fit because, we [Insert problem that the user’s startup is solving]"""
    )
]

LAST_RESPONSE_INDIVIDUAL_EMAIL = [
    ResponseSchema(
        name="Individual email message",
        description="""Write a paragraph that can inserted to an email to the analyst, the objective of this paragraph is to show that the investor has invested in a company that are similar to the  user’s startup. Therefore, write paragraph as follow: “I notice that you have invested in [insert the name and website url of the first startup that solve very similar problems] and [insert the name and website url of the second  startup that solve very similar problems] which are focus on [Insert the problem they are solving], seeing this I think we could be a great fit because, we [Insert problem that the user’s startup is solving]"""
    )
]
