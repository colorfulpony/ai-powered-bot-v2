import json
from fuzzywuzzy import fuzz
from langchain.tools.json.tool import JsonSpec

def find_matching_vcs_id(user_industries, user_stages, json_data):
    matching_vc_ids = []

    venture_capitals = json_data.get("venture_capitals")
    if venture_capitals:
        for vc_data in venture_capitals:
            for vc_name, vc_details in vc_data.items():
                vc_industries = vc_details.get("vc_industries")
                vc_stages = vc_details.get("vc_stages")
                if vc_industries:
                    vc_industries_lower = [industry.lower().strip() for industry in vc_industries.split(",")]
                    user_industries_lower = [industry.lower().strip() for industry in user_industries.split(",")]

                    max_similarity_industry = 0
                    max_similarity_stage = 0

                    for user_industry in user_industries_lower:
                        for industry in vc_industries_lower:
                            similarity = fuzz.ratio(user_industry, industry)
                            if similarity > max_similarity_industry:
                                max_similarity_industry = similarity

                    if vc_stages:
                        vc_stages_lower = [stage.lower().strip() for stage in vc_stages.split(",")]
                        user_stages_lower = [stage.lower().strip() for stage in user_stages.split(",")]
                        for user_stage in user_stages_lower:
                            for stage in vc_stages_lower:
                                similarity = fuzz.ratio(user_stage, stage)
                                if similarity > max_similarity_stage:
                                    max_similarity_stage = similarity

                    if vc_stages:
                        if max_similarity_industry >= 55 and max_similarity_stage >= 80:  # Adjust the similarity threshold as per your preference
                            vc_id = vc_details.get("vc_id")
                            matching_vc_ids.insert(0, vc_id)
                    else:
                        if max_similarity_industry >= 55:  # Adjust the similarity threshold as per your preference
                            vc_id = vc_details.get("vc_id")
                            matching_vc_ids.append(vc_id)

    return matching_vc_ids

def main():
    with open("./json/test.json") as f:
        data = json.load(f)

    user_industries = "Healthcare, Technology, AI"  # Comma-separated list of industries
    user_stages = "Seed"  # Comma-separated list of industries
    filtered_data = find_matching_vcs_id(user_industries, user_stages, data)

if __name__ == "__main__":
    main()