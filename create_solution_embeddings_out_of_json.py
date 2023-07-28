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


with open('jsons/main_test.json') as f:
    data = json.load(f)

# Process each VC name and details in the data
for vc_name, vc_info in data.items():
    # Create an empty list to store the startup names and solutions
    df_solutions = pd.DataFrame(columns=['vc_startup', 'vc_startup_solution'])

    # Create lists to store the startup names and solutions
    startup_names = []
    startup_solutions = []

    # Iterate over each startup in the VC's portfolio
    for startup in vc_info['vc_portfolio']:
        startup_name = startup['vc_portfolio_startup_name']
        startup_solution = startup['vc_portfolio_startup_solution']
        startup_names.append(startup_name)
        startup_solutions.append(startup_solution)

    # Create a DataFrame from the startup data
    df_temp = pd.DataFrame({'vc_startup': startup_names, 'vc_startup_solution': startup_solutions})

    # Concatenate the temporary dataframe with the main industries dataframe
    df_solutions = pd.concat([df_solutions, df_temp], ignore_index=True)

    # Create a filename based on the VC name
    filename = vc_name.lower().replace(" ", "_") + ".csv"

    # Ensure the input is a string and get embeddings for each industry
    df_solutions['embedding'] = df_solutions['vc_startup_solution'].apply(lambda x: get_embedding(str(x)))

    # Save the dataframe to a CSV file
    df_solutions.to_csv("embeddings/solutions_embeddings/" + filename)
