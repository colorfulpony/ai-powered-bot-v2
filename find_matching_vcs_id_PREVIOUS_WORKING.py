import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def find_matching_vcs_id(user_industries, user_stages, json_data):
    matching_vc_ids = []

    venture_capitals = json_data.get("venture_capitals")
    if venture_capitals:
        for vc_data in venture_capitals:
            for vc_name, vc_details in vc_data.items():
                vc_industries = vc_details.get("vc_industries")
                vc_stages = vc_details.get("vc_stages")

                if vc_industries != "-" and vc_industries != "":
                    vc_industries_lower = [industry.lower().strip() for industry in vc_industries.split(",")]
                    user_industries_lower = [industry.lower().strip() for industry in user_industries.split(",")]

                    industry_match = any(is_industry_match(vc_industry, user_industries_lower) for vc_industry in vc_industries_lower)

                    if vc_stages != "-" and vc_stages != "":
                        vc_stages_lower = [stage.lower().strip() for stage in vc_stages.split(",")]
                        user_stages_lower = [stage.lower().strip() for stage in user_stages.split(",")]

                        stage_match = any(is_industry_match(vc_stage, user_stages_lower) for vc_stage in vc_stages_lower)

                        if industry_match and stage_match:
                            vc_id = vc_details.get("vc_id")
                            matching_vc_ids.insert(0, vc_id)
                    else:
                        if industry_match:
                            vc_id = vc_details.get("vc_id")
                            matching_vc_ids.append(vc_id)
                else:
                    continue

    return matching_vc_ids


def is_industry_match(industry_vc, industries_startup, threshold=0.5):
    embeddings = model.encode([industry_vc] + industries_startup)
    similarities = cosine_similarity([embeddings[0]], embeddings[1:])
    return any(similarity >= threshold for similarity in similarities[0])


def main():
    with open("json/main.json") as f:
        data = json.load(f)

    user_industries = "FinTech"  # Comma-separated list of industries
    user_stages = "Seed"  # Comma-separated list of stages
    filtered_data = find_matching_vcs_id(user_industries, user_stages, data)
    print(filtered_data)


if __name__ == "__main__":
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    main()
