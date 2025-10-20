from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from http.cookiejar import MozillaCookieJar
from bs4 import BeautifulSoup
import time

link = "https://www.linkedin.com/jobs/search/?keywords=data%20scientist&f_TPR=r40000&sortBy=DD&origin=JOB_SEARCH_PAGE_JOB_FILTER"

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.get("https://www.linkedin.com/") 
jar = MozillaCookieJar()
jar.load('cookies.txt', ignore_discard=True, ignore_expires=True)

for cookie in jar:
    cookie_dict = {
        'name': cookie.name,
        'value': cookie.value,
        'domain': cookie.domain.lstrip('.'),
        'path': cookie.path,
    }
    if cookie.expires:
        cookie_dict['expiry'] = int(cookie.expires)
    try:
        driver.add_cookie(cookie_dict)
    except Exception as e:
        pass

driver.get(link)
time.sleep(5)

with open('jobs.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)

driver.quit()

with open('jobs.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

job_listings = soup.find_all('li', {'data-occludable-job-id': True})

if job_listings:
    for job in job_listings[:10]:
        title_element = job.find('a', class_='job-card-container__link')
        company_element = job.find('div', class_='artdeco-entity-lockup__subtitle')
        location_element = job.find('div', class_='artdeco-entity-lockup__caption')

        if title_element and company_element and location_element:
            title = title_element.text.strip()
            company = company_element.text.strip()
            location = location_element.text.strip()
            link = title_element['href']
            if link.startswith('/'):
                link = "https://www.linkedin.com" + link

            print(f"Title: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print(f"Link: {link}")
            print("-" * 20)