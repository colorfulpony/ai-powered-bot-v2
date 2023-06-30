import os
import openai
import pandas as pd
import json
import time


# Access the API key and use it in API requests
openai.api_key = os.environ["OPENAI_API_KEY"]


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    retries = 3
    for attempt in range(retries):
        try:
            # Get the embedding for the text using the specified model
            return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e


with open('jsons/main.json') as f:
    data = json.load(f)

# Process each VC name and details in the data
for vc_name, vc_details in data.items():
    df_industries = pd.DataFrame(columns=['vc_industry'])

    vc_industries = vc_details['vc_industries'].split(',')

    # Create a temporary dataframe for the VC industries
    df_temp = pd.DataFrame({'vc_industry': vc_industries})

    # Concatenate the temporary dataframe with the main industries dataframe
    df_industries = pd.concat([df_industries, df_temp], ignore_index=True)

    # Create a filename based on the VC name
    filename = vc_name.lower().replace(" ", "_") + ".csv"

    # Ensure the input is a string and get embeddings for each industry
    df_industries['embedding'] = df_industries['vc_industry'].apply(lambda x: get_embedding(str(x)))

    # Save the dataframe to a CSV file
    df_industries.to_csv("industry_embeddings/" + filename)
