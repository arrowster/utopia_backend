import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

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


def get_soup_wait_class_element(driver, url, class_name, is_scrolling):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
        time.sleep(1)
    except Exception as e:
        e
        return False
    time.sleep(random.randint(2, 7))
    if is_scrolling:
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            actions = ActionChains(driver)
            actions.send_keys(Keys.END).perform()
            time.sleep(random.randint(1, 4))

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def get_soup_from_url(driver, url):
    driver.get(url)
    current_url = driver.current_url
    if current_url == 'https://www.auction.co.kr/':  # 옥션 마켓이 없으면 여기로 리다이렉션 됨
        return False
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'div'))
        )
    except Exception as e:
        e
        return False

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        actions = ActionChains(driver)
        actions.send_keys(Keys.END).perform()
        time.sleep(random.randint(1, 3))

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup
