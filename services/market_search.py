import os.path
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utopia_backend.services.SingletonWebDriver import get_soup_from_url


def gmarket_search(driver, words):
    for word in words:
        shop_set = set()
        url = f'https://www.gmarket.co.kr/n/search?keyword={word}&f=o:i&k=0&p=1&v=l'
        soup = get_soup_from_url(driver, url)
        product_items = soup.find_all('a', class_='link__shop')

        for item in product_items:
            if item and 'href' in item.attrs:
                shop_url = item['href']
                shop_set.add(shop_url)
            else:
                print("가게 링크를 찾을 수 없습니다.")

    shop_list = list(shop_set)
    return shop_list
