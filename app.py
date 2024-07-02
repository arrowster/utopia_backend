import os
import time

from urllib.parse import quote
from flask import Flask
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from routers import routers
from services.SingletonWebDriver import SingletonWebDriver
from services import market_search
from services.pruning_shop_item import pruning_shop_item
from services.save_urls_image_in_directory import save_urls_image_in_directory

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/test-signal')
def test_sig_func():
    return routers.test_signal()


@app.route('/market-search')
def market_search_func():
    driver = SingletonWebDriver.get_driver()
    min_price = None
    max_price = None

    keywordlist = routers.key_words()
    print(keywordlist)
    #todo: web띄워서 타오바오 로그인 url 보여주기
    # 로그인 완료 서버에 알려줘야함...
    shop_list = market_search.gmarket_search(driver, keywordlist)
    print(shop_list)
    shop_items = pruning_shop_item(driver, shop_list, min_price, max_price)
    print(f'{shop_items},\r\n'
          f'{len(shop_items)}개')

    image_urls = [item.image_url for item in shop_items]
    save_urls_image_in_directory(image_urls)


    #for i in range(3):
    #    path = f'./temp_img/{i}.jpg'
    #    market_search.taobao_image_search(driver, path)
    #todo: keyword 가지치기
    # url 이미지 다운로드
    # taobao 이미지 검색
    # url 3개 씩 뽑아오기
    #todo: 배송비 측정

    print('close webDriver')
    SingletonWebDriver.close_driver()
    return keywordlist


if __name__ == '__main__':
    app.run()
