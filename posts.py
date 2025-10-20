from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from http.cookiejar import MozillaCookieJar
from bs4 import BeautifulSoup
import time

link = "https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords=web%20developer&origin=FACETED_SEARCH&sid=%3AIL&sortBy=%22date_posted%22"
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
print("Scrolling to load posts...")
last_height = driver.execute_script("return document.body.scrollHeight")

for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("Finished scrolling, saving page...")
time.sleep(3)
with open('posts.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)

driver.quit()

with open('posts.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
post_listings = soup.select('ul.UxCmIibYAONlcZPmrRSKxZmEzOkAdVojokcPfA > li.artdeco-card div[data-urn^="urn:li:activity:"]')

if post_listings:
    for post_container in post_listings:
        actor_meta_div = post_container.find('div', class_='update-components-actor__meta')
        content_div = post_container.find('div', class_='update-components-text')
        actor_link_element = actor_meta_div.find('a', class_='update-components-actor__meta-link')
        link = actor_link_element.get('href', 'Not Found')
        if link.startswith('/'):
            link = "https://www.linkedin.com" + link

        actor_span = actor_link_element.find('span', class_='update-components-actor__title')
        name_span = actor_span.find('span', {'aria-hidden': 'true'})
        actor = name_span.text.strip()
                    

        content_span = content_div.find('span', dir='ltr')
        content = content_span.get_text(separator=' ', strip=True)
 
        print(f"Actor: {actor}")
        print(f"Content: {content}")
        print(f"Link: {link}")
        print("-" * 20)
