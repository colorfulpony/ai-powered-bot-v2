import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


def scrap_portfolio_website(url: str) -> str:
    text = ""
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--headless')
    options.add_argument("--user-data-dir=C:/Users/flexy/AppData/Local/Google/Chrome/User Data/Default")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (iPad; CPU OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/98.0.4758.99 Mobile/15E148 Safari/604.1")

    driver = webdriver.Chrome(options=options)

    try:
        status_code = get_status_code(url)
        if 200 <= status_code < 300:
            driver.get(url)
            text = driver.find_element(By.TAG_NAME, 'body').text
    except Exception as e:
        print(f"Error occurred while scraping portfolio website: {str(e)}")
    finally:
        driver.quit()

    return text
