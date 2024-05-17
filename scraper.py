import time
import random  # Import the random module
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
from urllib.parse import quote_plus  # Import for URL encoding

def scroll_page(url):
    service = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--lang=en")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    old_height = driver.execute_script("""
        function getHeight() {
            return document.querySelector('.zxU94d').scrollHeight;
        }
        return getHeight();
    """)

    while True:
        driver.execute_script("document.querySelector('.zxU94d').scrollTo(0, document.querySelector('.zxU94d').scrollHeight)")

        time.sleep(2)

        new_height = driver.execute_script("""
            function getHeight() {
                return document.querySelector('.zxU94d').scrollHeight;
            }
            return getHeight();
        """)

        if new_height == old_height:
            break

        old_height = new_height

    selector = Selector(driver.page_source)
    driver.quit()

    return selector

def scrape_google_jobs(selector, search_url):
    google_jobs_results = []

    for result in selector.css('.iFjolb'):
        title = result.css('.BjJfJf::text').get()
        company = result.css('.vNEEBe::text').get()

        container = result.css('.Qk80Jf::text').getall()
        location = container[0]
        via = container[1]

        thumbnail = result.css('.pJ3Uqf img::attr(src)').get()
        extensions = result.css('.KKh3md span::text').getall()

        # Extracting the job link
        link = result.css('a.BjJfJf::attr(href)').get()
        if link and not link.startswith('http'):
            link = 'https://www.google.com' + link
        else:
            # Fallback to a Google search URL if job-specific link is not found
            query = quote_plus(f"{title} {company}")
            link = f"https://www.google.com/search?q={query}"

        google_jobs_results.append({
            'title': title,
            'company': company,
            'location': location,
            'via': via,
            'thumbnail': thumbnail,
            'extensions': extensions,
            'link': link
        })

    random.shuffle(google_jobs_results)  # Shuffle the job listings
    return google_jobs_results

def selenium_scrape():
    params = {
        'q': 'microbiologist',  # search string
        'ibp': 'htl;jobs',  # google jobs
        'uule': 'w+CAIQICIFSW5kaWE',  # encoded location (USA)
        'hl': 'en',  # language
        'gl': 'india',  # country of the search
    }

    URL = f"https://www.google.com/search?q={params['q']}&ibp={params['ibp']}&uule={params['uule']}&hl={params['hl']}&gl={params['gl']}"

    result = scroll_page(URL)
    return scrape_google_jobs(result, URL)
