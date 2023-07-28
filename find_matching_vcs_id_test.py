import os
import json
from dotenv import load_dotenv
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import openai


# Access the API key and use it in API requests
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


def calculate_similarity(embedding1, embedding2):
    """
    Calculates the cosine similarity between two embeddings.

    Args:
        embedding1 (array-like): First embedding.
        embedding2 (array-like): Second embedding.

    Returns:
        float: Cosine similarity between the two embeddings.
    """
    return cosine_similarity([embedding1], [embedding2])[0][0]


def get_embedding(text, model="text-embedding-ada-002"):
    """
    Retrieves the embedding for a given text using the OpenAI API.

    Args:
        text (str): Input text to be embedded.
        model (str): Model name for embedding. Defaults to "text-embedding-ada-002".

    Returns:
        array-like: Embedding representation of the input text.
    """
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def insert_dict_sorted(existing_list, new_dict):
    """
    Inserts a dictionary into a sorted list based on a specific key.

    Args:
        existing_list (list): Existing list of dictionaries.
        new_dict (dict): New dictionary to be inserted.

    Returns:
        list: Updated list with the new dictionary inserted in the correct position.
    """
    if len(existing_list) == 0:
        existing_list.append(new_dict)
        return existing_list

    for i, dict_item in enumerate(existing_list):
        if new_dict['matching_score'] > dict_item['matching_score']:
            existing_list.insert(i, new_dict)
            break
    else:
        existing_list.append(new_dict)

    return existing_list


def find_matching_vcs(user_solution, json_data):
    """
    Finds venture capitals (VCs) that match the given user industries and stages.

    Args:
        user_industries (list): List of user industries.
        user_stages (list): List of user stages.
        json_data (dict): JSON data containing VC details.

    Returns:
        list: List of matching VC IDs sorted by matching score.
    """
    matching_vc_ids = []

    # Get embeddings for user industries
    user_solution_embedding = get_embedding(user_solution)

    # Get embeddings for user stages

    for vc_name, vc_details in json_data.items():
        fund_solution_sco = 0

        filename = vc_name.lower().replace(" ", "_") + ".csv"

        # Read industry embeddings from CSV file
        df_solution = pd.read_csv("embeddings/solutions_embeddings/" + filename)
        df_solution['embedding'] = df_solution['embedding'].apply(eval).apply(np.array)

        for solution_df_index, solution_df_row in df_solution.iterrows():
            solution_score = calculate_similarity(user_solution_embedding, solution_df_row['embedding'])
            print(f"""Startup solution - {solution_df_row['vc_startup_solution']}
Score - {solution_score}""")

def main():
    # Load JSON data
    with open("jsons/main_test.json") as f:
        data = json.load(f)

    # Define user industries and stages
    startup_solution = "It solves the user problem of automating key areas of business operations such as invoicing, payment collections, bulk payouts, GST filing, and customer data management."

    # Find matching VCs
    matching_vc_ids = find_matching_vcs(startup_solution, data)


if __name__ == "__main__":
    main()
