import requests
import random


def get_status_code(url: str) -> int:
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error occurred while making the HTTP request: {str(e)}")
        return 0


def scrap_portfolio_website(url: str, browser) -> str:
    text = "-"

    # try:
    #     with open("user-agents.txt", 'r') as file:
    #         user_agents = file.read().splitlines()
    # except FileNotFoundError:
    #     print("user-agents.txt file not found.")
    #     return text

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"

    try:
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": user_agent})

        status_code = get_status_code(url)
        if 200 <= status_code < 300:
            page.goto(url)
            text = page.inner_text('body')
    except Exception as e:
        print(f"Error occurred while scraping portfolio website: {str(e)}")
    finally:
        page.close()

    return text
