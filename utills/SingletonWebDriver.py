import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class SingletonWebDriver:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonWebDriver, cls).__new__(cls)
            cls._instance._init_driver()
        return cls._instance

    def _init_driver(self):
        user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/73.0.3683.86 Safari/537.36')

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("disable-infobars")
        options.add_argument('incognito')
        options.add_argument("window-size=800,700")
        options.add_argument(f'user-agent={user_agent}')

        service = Service()
        self.driver = webdriver.Chrome(service=service, options=options)
        
    @classmethod
    def get_driver(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance.driver
    
    @classmethod
    def close_driver(cls):
        print('close webdriver')
        if cls._instance and cls._instance.driver:
            cls._instance.driver.quit()
            cls._instance = None


def get_soup_from_url(driver, url):
    driver.get(url)
    body = driver.find_element(By.CSS_SELECTOR, 'body')

    try:
        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_all_elements_located((By.TAG_NAME, 'div'))
        )
    except Exception as e:
        print("페이지 로드 중 오류 발생:", e)
        return False

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    return soup
