import os
import openai
import pandas as pd
import json
import time

openai.api_key = os.environ["OPENAI_API_KEY"]


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    retries = 3
    for attempt in range(retries):
        try:
            return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e


with open('json/main.json') as f:
    data = json.load(f)
    data = data.get("venture_capitals")

for vc_data in data:
    for vc_name, vc_details in vc_data.items():
        df_industries = pd.DataFrame(columns=['vc_industry'])

        vc_industries = vc_details['vc_industries'].split(',')

        df_temp = pd.DataFrame({'vc_industry': vc_industries})
        df_industries = pd.concat([df_industries, df_temp], ignore_index=True)

        filename = vc_name.lower().replace(" ", "_") + ".csv"

        # Ensure the input is a string
        df_industries['embedding'] = df_industries['vc_industry'].apply(lambda x: get_embedding(str(x)))
        df_industries.to_csv("industry_embeddings/" + filename)