import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def initialize_driver():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("window-size=10,10")
    options.add_argument(f'user-agent={user_agent}')

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def get_soup_from_url(driver, url):
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
        return None

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    return soup
