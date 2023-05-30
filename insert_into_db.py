from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine, text

# Initialize Connector object
connector = Connector()

# Function to return the database connection
def getconn():
    conn = connector.connect(
        "ai-powered-bot-filling-db:us-central1:ai-powered-bot-data",
        "pymysql",
        user="root",
        password="Mak7ka321.",
        db="ai-powered-bot"
    )
    return conn

def insert_data_into_db(vc_name, vc_website_url, vc_linkedin_url, vc_investor_name, vc_investor_email, vc_stages, vc_industries, portfolio_websites_data):
    # Create connection pool
    pool = create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )

    # Insert data queries
    vc_insert_query = text(f'INSERT INTO venture_capital (name, website_url, linkedin_url, industries, stages) VALUES ("{vc_name}", "{vc_website_url}", "{vc_linkedin_url}", "{vc_industries}", "{vc_stages}");')
    analyst_insert_query = text(f'INSERT INTO analyst (name, email) VALUES ("{vc_investor_name}", "{vc_investor_email}");')

    # Interact with Cloud SQL database using connection pool
    with pool.connect() as db_conn:
        # Execute venture capital insertion query
        db_conn.execute(vc_insert_query)
        # Retrieve the last inserted venture capital ID
        venture_capital_id = db_conn.execute(text("SELECT LAST_INSERT_ID();")).scalar()


        if portfolio_websites_data is not None:
            for portfolio_website in portfolio_websites_data:
                pw_insert_query = text(f'INSERT INTO portfolio_website (name, website_url, solution) VALUES ("{portfolio_website[0]}", "{portfolio_website[1]}", "{portfolio_website[2]}");')

                # Execute portfolio website insertion query
                db_conn.execute(pw_insert_query)
                # Retrieve the last inserted portfolio website ID
                portfolio_website_id = db_conn.execute(text("SELECT LAST_INSERT_ID();")).scalar()

                # Insert data into the portfolio_website_has_venture_capital table
                pw_vc_query = text(f'INSERT INTO portfolio_website_has_venture_capital (portfolio_website_id, venture_capital_id) VALUES ("{portfolio_website_id}", "{venture_capital_id}");')
                db_conn.execute(pw_vc_query)

        # Execute analyst insertion query
        db_conn.execute(analyst_insert_query)
        # Retrieve the last inserted analyst ID
        analyst_id = db_conn.execute(text("SELECT LAST_INSERT_ID();")).scalar()

        # Insert data into the venture_capital_has_analyst table
        vc_analyst_query = text(f'INSERT INTO venture_capital_has_analyst (venture_capital_id, analyst_id) VALUES ("{venture_capital_id}", "{analyst_id}");')
        db_conn.execute(vc_analyst_query)

        result = db_conn.execute(text('SELECT * FROM venture_capital;')).fetchall()

        print(result)


if __name__ == '__main__':
    insert_data_into_db("VC 3", "VC3.com", "linkedin.com/vc3", "VC Investor 3", "vc3investor@gmail.com", "VC 3 Stages", "VC 3 Industries", [("STartup 1", 'starrtup1.com', 'some solution1'), ("STartup 2", 'starrtup2.com', 'some solution2'), ("STartup 3", 'starrtup3.com', 'some solution3')])
