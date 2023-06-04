from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import random

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

# user_agents = load_user_agents()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"


async def collect_links_with_playwright(url, starting_domain, browser):
    page = await browser.new_page()
    await page.set_extra_http_headers({"User-Agent": user_agent})
    await page.goto(url)

    links = []
    elements = await page.query_selector_all('a')
    for element in elements:
        link = await element.get_attribute('href')
        if link and not any(link.startswith(delete_url) for delete_url in DELETE_URL_THAT_STARTS_WITH) and urlparse(link).netloc != starting_domain:
            if link.startswith("http://"):
                link = link.replace("http://", "https://")
            if not link.startswith("https://"):
                continue
            links.append(link)
    await page.close()
    return links


async def collect_all_links(url, browser):
    starting_domain = urlparse(url).netloc
    links = set()

    # Collect links using Playwright
    try:
        playwright_links = await collect_links_with_playwright(url, starting_domain, browser)
        links.update(playwright_links)
    except Exception as e:
        text = ""
        # print(f"Error occurred while collecting links with Playwright: {str(e)}")
    return links


async def get_portfolio_links(url, browser):
    all_links = await collect_all_links(url, browser)

    # Remove duplicate links
    unique_links = list(set(all_links))

    return unique_links
