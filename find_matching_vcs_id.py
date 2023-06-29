import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import openai


def calculate_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def insert_dict_sorted(existing_list, new_dict):
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
    matching_vc_ids = []
    venture_capitals = json_data.get("venture_capitals")

    user_industries_embeddings = [{"user_industry": user_industry, "embedding": get_embedding(user_industry)} for user_industry in user_industries]
    user_stages_embeddings = [{"user_stage": user_stage, "embedding": get_embedding(user_stage)} for user_stage in user_stages]

    if venture_capitals:
        for vc_data in venture_capitals:
            for vc_name, vc_details in vc_data.items():
                fund_industry_stage_score = 0

                filename = vc_name.lower().replace(" ", "_") + ".csv"

                df_industries = pd.read_csv("industry_embeddings/" + filename)
                df_industries['embedding'] = df_industries['embedding'].apply(eval).apply(np.array)

                df_stages = pd.read_csv("stage_embeddings/" + filename)
                df_stages['embedding'] = df_stages['embedding'].apply(eval).apply(np.array)

                for user_industry_embedding in user_industries_embeddings:
                    for industry_df_index, industry_df_row in df_industries.iterrows():
                        industry_score = calculate_similarity(user_industry_embedding['embedding'], industry_df_row['embedding'])
                        if industry_score >= 0.88:
                            fund_industry_stage_score += 1
                        print(f"User Industry - {user_industry_embedding['user_industry']} + VC Industry - {industry_df_row['vc_industry']} => Score - {industry_score}")

                for user_stage_embedding in user_stages_embeddings:
                    for stage_df_index, stage_df_row in df_stages.iterrows():
                        stage_score = calculate_similarity(user_stage_embedding['embedding'], stage_df_row['embedding'])
                        if stage_score >= 0.95:
                            fund_industry_stage_score += 0.1

                vc_id_with_matching_score = {'vc_id': vc_details['vc_id'], 'matching_score': fund_industry_stage_score}
                if fund_industry_stage_score >= 1:
                    matching_vc_ids = insert_dict_sorted(matching_vc_ids, vc_id_with_matching_score)

            print(matching_vc_ids)
    return matching_vc_ids


def main():
    with open("json/main.json") as f:
        data = json.load(f)

    startup_industries = ["AI", "E-commerce", "Climate Tech"]
    startup_stages = ["Seed"]
    matching_vc_ids = find_matching_vcs(startup_industries, startup_stages, data)


if __name__ == "__main__":
    main()
