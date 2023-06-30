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
    df_stages = pd.DataFrame(columns=['vc_stage'])

    vc_stages = vc_details['vc_stages'].split(',')

    # Create a temporary dataframe for the VC stages
    df_temp = pd.DataFrame({'vc_stage': vc_stages})

    # Concatenate the temporary dataframe with the main stages dataframe
    df_stages = pd.concat([df_stages, df_temp], ignore_index=True)

    # Create a filename based on the VC name
    filename = vc_name.lower().replace(" ", "_") + ".csv"
    print(filename)

    # Ensure the input is a string and get embeddings for each stage
    df_stages['embedding'] = df_stages['vc_stage'].apply(lambda x: get_embedding(str(x)))

    # Save the dataframe to a CSV file
    df_stages.to_csv("stage_embeddings/" + filename)
    print(df_stages)
