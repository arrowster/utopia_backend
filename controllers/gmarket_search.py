import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup


def gmarket_search(words):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("window-size=10,10")
    options.add_argument('user-agent=' + user_agent)

    driver = webdriver.Chrome(service=service, options=options)

    for word in words:
        shop_set = set()
        url = f'https://www.gmarket.co.kr/n/search?keyword={word}&f=o:i&k=0&p=1&v=l'
        driver.get(url)

        body = driver.find_element(By.CSS_SELECTOR, 'body')
        body.send_keys(Keys.END)
        time.sleep(1)
        try:
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_all_elements_located((By.TAG_NAME, 'div'))
            )
        except Exception as e:
            print("페이지 로드 중 오류 발생:", e)
            driver.quit()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_items = soup.find_all('a', class_='link__shop')
        print(product_items)

        for item in product_items:
            if item and 'href' in item.attrs:
                shop_url = item['href']
                shop_set.add(shop_url)
            else:
                print("가게 링크를 찾을 수 없습니다.")

    driver.quit()
    shop_list = list(shop_set)
    print(shop_list)
    return shop_list
