from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


DELETE_URL_THAT_STARTS_WITH = (
   'https://b12.io', 'https://www.linkedin.com', 'https://vimeo.com',
   'https://www.google.com', 'https://services', 'https://www.twitter.com',
   'https://www.pingidentity.com', 'https://goo', 'https://www.facebook.com',
   'https://instagram.com', 'https://www.crunchbase.com/', 'https://angel.co/',
   'https://www.producthunt.com/', 'https://www.techcrunch.com/',
   'https://www.forbes.com/', 'https://www.bloomberg.com/',
   'https://www.reuters.com/', 'https://www.wsj.com/', 'https://www.nytimes.com/',
   'https://www.cnbc.com/', 'https://www.barrons.com/',
   'https://www.businessinsider.com/', 'https://www.inc.com/',
   'https://www.fastcompany.com/', 'https://www.wired.com/',
   'https://www.entrepreneur.com/', 'https://www.ycombinator.com/', 'https://500.co/',
   'https://www.seedcamp.com/', 'https://www.accel.com/', 'https://www.greylock.com/',
   'https://www.indexventures.com/', 'https://www.kleinerperkins.com/',
   'https://www.greylock.com/', 'https://www.benchmark.com/',
   'https://www.socialcapital.com/', 'https://www.softbank.com/',
   'https://www.samsung.com/us/', 'https://www.qualcomm.com/', 'https://www.ibm.com/',
   'https://www.microsoft.com/', 'https://aws.amazon.com/', 'https://www.google.com/',
   'https://www.apple.com/', 'https://www.facebook.com/', 'https://www.twitter.com/',
   'https://www.linkedin.com/', 'https://www.instagram.com/', 'https://www.youtube.com/',
   'https://vimeo.com/', 'https://www.slideshare.net/', 'https://www.quora.com/',
   'https://medium.com/', 'https://www.reddit.com/', 'https://www.stackoverflow.com/',
   'https://www.github.com/', 'https://www.codepen.io/', 'https://dribbble.com/',
   'https://www.behance.net/', 'https://www.figma.com/', 'https://www.invisionapp.com/',
   'https://www.intercom.com/', 'https://www.mixpanel.com/', 'https://www.optimizely.com/',
   'https://www.pingdom.com/', 'https://www.pingidentity.com/', 'https://www.cloudflare.com/',
   'https://www.akamai.com/', 'https://www.salesforce.com/', 'https://www.hubspot.com/',
   'https://www.marketo.com/', 'https://www.mailchimp.com/', 'https://www.zendesk.com/',
   'https://www.atlassian.com/', 'https://slack.com/', 'https://www.dropbox.com/',
   'https://www.box.com/', 'https://www.google.com/drive/', 'https://www.icloud.com/',
   'https://trello.com/', 'https://www.notion.so/', 'https://www.asana.com/',
   'https://www.todoist.com/', 'https://www.evernote.com/', 'https://www.nike.com/',
   'https://www.adidas.com/', 'https://www.underarmour.com/', 'https://www.lululemon.com/',
   'https://www.gap.com/', 'https://www.zara.com/', 'https://www.hm.com/', 'https://www.amazon.com/',
   'https://www.walmart.com/', 'https://www.target.com/', 'https://www.bestbuy.com/',
   'https://www.costco.com/', 'https://www.netflix.com/', 'https://www.hulu.com/',
   'https://www.disneyplus.com/', 'https://www.primevideo.com/', 'https://www.hbo.com/',
   'https://www.spotify.com/', 'https://www.apple.com/apple-music/', "/", "#", "https://docs.google.com/",
   "https://twitter.com/", "mailto:", "https://techcrunch.com/",
)


def collect_links_with_selenium(url, starting_domain):
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
    driver.get(url)

    links = []
    elements = driver.find_elements(By.TAG_NAME, 'a')
    for element in elements:
        link = element.get_attribute('href')
        if link and not any(link.startswith(delete_url) for delete_url in DELETE_URL_THAT_STARTS_WITH) and urlparse(link).netloc != starting_domain:
            links.append(link)
    return links


def collect_all_links(url):
    starting_domain = urlparse(url).netloc
    links = set()

    # Collect links using Selenium
    try:
        selenium_links = collect_links_with_selenium(url, starting_domain)
        links.update(selenium_links)
    except Exception as e:
        print(f"Error occurred while collecting links with Selenium: {str(e)}")
    return links


def get_portfolio_links(url):
    all_links = collect_all_links(url)

    # Remove duplicate links
    unique_links = list(set(all_links))

    # Print all the collected links
    for link in unique_links:
        print(link)

    return unique_links
