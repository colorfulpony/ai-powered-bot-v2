from langchain.output_parsers import ResponseSchema

# main vc
INDUSTRIES_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Industries in which the fund invests",
        description="""Analyze the context given to you and find the industries in which this investment fund invests. Use only those industries that I wrote below.

        Output format:
        abs, xyz, asd

        Here is a list of all possible investment industries: Technology, E-commerce, Healthcare, Finance, Education, Food, Beverage, Energy, Travel, Hospitality, Real Estate, Entertainment, Social Impact, Marketing, Advertising, Transportation, Logistics, Manufacturing, Agriculture, Fashion, Beauty, Personal Care, Fitness, Wellness, Home Services, Construction, Engineering, Automotive, Sports, Recreation, Art, Design, Media, Publishing, Government, Public Services, Professional Services, HR, Recruitment, Gaming, Esports, Insurance, Telecommunications, Security, Surveillance, Aerospace, Defense, Biotechnology, Pharmaceuticals, Chemicals, Consumer Electronics, Consumer Goods, Environmental Services, Hospitality, Events, Industrial Automation, Robotics, Legal Services, Materials Science, Medical Devices, Mining, Metals, Nanotechnology, Packaging, Containers, Plastics, Rubber, Retail, Social Media, Networking, Software, IT Services, Supply Chain, Logistics, Virtual, Augmented Reality, Crowdfunding, Fundraising, Internet of Things, Smart Homes, Robotics, Drones, AI, Machine Learning, Blockchain, Cryptocurrency, Quantum Computing, Space Exploration, Commercialization, Urban Farming, Agriculture, Waste Management, Recycling, Water, Waste Treatment, 3D Printing, Additive Manufacturing, Architecture, Design, Cloud Computing, Databases, Information Management, Design, User Experience, Digital Signage, Display Advertising,DTC Products, Distributed Ledger Technology, Document Management, Automation, Employee Benefits, Perks, Event Planning, Management, Facility Management, Maintenance, Financial Technology, Services, Fleet Management, Transportation Services, Food Delivery, Meal Kits, Health, Fitness Wearables, Home Security, Surveillance, Identity, Access Management, Influencer Marketing, Social Media Advertising, Intellectual Property Management, Internet Services, ISPs, Legal Tech, Services, Logistics, Supply Chain Management, Marketing Automation, Analytics, Medical Research, Development, Online Learning Platforms, MOOCs, Online Marketplaces, Auctions, Personalized Nutrition, Wellness, Privacy, Data Security, Procurement, Vendor Management, Product Design, Development, Professional Development, Training, Property Management, Maintenance, Public Relations, Communications, Renewable Energy, Clean Tech, Smart City, Infrastructure, Wearable Technology, IoT Devices, Advanced Materials, Agritech, Air Quality Control, Animal Health, Nutrition, App Development, Design, Asset Management, Investment, Audio, Music, Autonomous Vehicles, Behavioral Analytics, Insights, Big Data, Analytics, Bioinformatics, Genomics, Business Intelligence, Analytics, Cloud Services, Infrastructure, Cognitive Computing, AI, Collaborative Tools, Workspaces, Commercial Real Estate, Communication, Networking, Computer Vision, Image Processing, Construction Tech, Building Materials, Corporate Social Responsibility,CRM, Cybersecurity, Privacy, Data Science, Analysis, Defense, Security, Digital Currency, Payments, Digital Marketing, Advertising, Digital Rights Management, Disaster Response, Relief, Diversity, Equity,, Inclusion (DEI), Document Collaboration, Sharing, Drones, Unmanned Aerial Vehicles (UAVs), E-commerce Platforms, Marketplaces, Education Technology, Services, Electric Vehicles, Charging Infrastructure, Electronic Components, Devices, Emerging Technologies, Innovation, Employee Engagement, Retention, Energy Storage, Distribution, Enterprise Resource Planning (ERP), Environmental Monitoring, Assessment, Event Ticketing, Management, Facility Maintenance, Management, Fashion Technology, Wearables, Financial Planning, Management, Fleet Maintenance, Management, Food Science, Technology, Fraud Detection, Prevention, Gaming, Gamification, Geo-location Services, Analytics, Graphic Design, Animation
        Your answer: """
    )
]

STAGES_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Stages in which the fund invests",
        description="""Analyze the context given to you and find the stages at which this investment fund invests. In your answer use only those stages that I wrote below.

        Output format:
        qwer, asdf, zxcv

        Here is a list of all possible investment stages: Idea Stage, Pre-Seed Stage, Seed Stage, Series A Stage, Series B Stage, Series C Stage, Series D Stage, Series E Stage, Late Stage, IPO Stage
        Your answer: """
    )
]

# vc portfolio startups
VC_PORTFOLIO_STARTUP_NAME_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Name of startup",
        description="""Analyze the context given to you and give me the name of the startup described in the context. Don't come up with any unreal names. I need only the real name based on the context
        
        Your answer: """
    )
]

VC_PORTFOLIO_STARTUP_SOLUTION_RESPONSE_SCHEMA = [
    ResponseSchema(
        name="Name of startup",
        description="""Analyze the context given to you and find out what user problems this startup is solving. Describe it briefly, clearly and simply. 5 sentences.
        
        Example of desired answer format:
        Startup aims to solve the problem of maintaining a healthy and beautiful garden for people who lack the time, knowledge, or resources to do it themselves. It provide a subscription-based service that offers regular visits from their trained gardeners who take care of all the necessary tasks such as watering, fertilizing, pruning, and pest control. They also use eco-friendly and sustainable practices to ensure a safe and healthy environment for both the plants and the customers. Their goal is to make gardening effortless and enjoyable for everyone, regardless of their experience level or busy schedules.

        Your answer: """
    )
]