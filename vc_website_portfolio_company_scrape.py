from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def scrap_portfolio_website(url: str) -> str:
    text = ""
    try:
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
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0")

        service = Service('C:/Users/flexy/PycharmProjects/pythonProject2/chromedriver.exe')
        service.start()
        driver = webdriver.Remote(service.service_url, options=options)
        text = driver.find_element(By.TAG_NAME, 'body').text
    except Exception as e:
        print(f"Error occurred while scraping portfolio website: {str(e)}")

    return text
