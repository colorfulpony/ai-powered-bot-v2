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


def find_matching_vcs(user_industries, user_stages, json_data):
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
    user_industries_embeddings = [{"user_industry": user_industry, "embedding": get_embedding(user_industry)} for user_industry in user_industries]

    # Get embeddings for user stages
    user_stages_embeddings = [{"user_stage": user_stage, "embedding": get_embedding(user_stage)} for user_stage in user_stages]

    for vc_name, vc_details in json_data.items():
        fund_industry_stage_score = 0

        filename = vc_name.lower().replace(" ", "_") + ".csv"

        # Read industry embeddings from CSV file
        df_industries = pd.read_csv("embeddings/industry_embeddings/" + filename)
        df_industries['embedding'] = df_industries['embedding'].apply(eval).apply(np.array)

        # Read stage embeddings from CSV file
        df_stages = pd.read_csv("embeddings/stage_embeddings/" + filename)
        df_stages['embedding'] = df_stages['embedding'].apply(eval).apply(np.array)

        # Calculate matching scores for user industries
        for user_industry_embedding in user_industries_embeddings:
            for industry_df_index, industry_df_row in df_industries.iterrows():
                industry_score = calculate_similarity(user_industry_embedding['embedding'], industry_df_row['embedding'])
                if industry_score >= 0.88:
                    print(f"User Industry - {user_industry_embedding['user_industry']} + VC Industry - {industry_df_row['vc_industry']} => Score - {industry_score}")
                    fund_industry_stage_score += 1
                    break

        # Calculate matching scores for user stages
        for user_stage_embedding in user_stages_embeddings:
            for stage_df_index, stage_df_row in df_stages.iterrows():
                stage_score = calculate_similarity(user_stage_embedding['embedding'], stage_df_row['embedding'])
                if stage_score >= 0.95:
                    fund_industry_stage_score += 0.1
                    break

        vc_id_with_matching_score = {'vc_id': vc_details['vc_id'], 'matching_score': fund_industry_stage_score}
        if fund_industry_stage_score >= 1:
            matching_vc_ids = insert_dict_sorted(matching_vc_ids, vc_id_with_matching_score)

    print(matching_vc_ids)
    return matching_vc_ids


def main():
    # Load JSON data
    with open("../jsons/main.json") as f:
        data = json.load(f)

    # Define user industries and stages
    startup_industries = ["AI", "E-commerce", "Climate Tech"]
    startup_stages = ["Seed"]

    # Find matching VCs
    matching_vc_ids = find_matching_vcs(startup_industries, startup_stages, data)


if __name__ == "__main__":
    main()
