import time

from flask import Flask
from routers import routers
from utills.SingletonWebDriver import SingletonWebDriver
from utills.save_image_and_return_abs_path import save_image_and_return_abs_path
from utills.get_abs_path import get_abs_path
from services import market_search
from services import taobao_search
from services.pruning_shop_item import pruning_shop_item

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
    taobao_url = 'https://s.taobao.com/search?q='
    min_price = None  # todo: 이것도 사용자에게 받아야함 생략 가능
    max_price = None

    keywordlist = routers.key_words()
    print(keywordlist)

    # 타오바오 로그인
    try:
        taobao_search.taobao_login(driver)
    except Exception as e:
        print("err:", e)
        print('close webDriver')
        SingletonWebDriver.close_driver()
        return e

    # 마켓 검색
    shop_list = market_search.gmarket_search(driver, keywordlist)
    print(shop_list)

    # 아이템 가지 치기
    shop_items = pruning_shop_item(driver, shop_list, min_price, max_price)
    print(f'{shop_items},\r\n'
          f'{len(shop_items)}개')

    # 타오바오 내에서 이미지 검색
    # 필요한 내용 크롤링(이미지, 상품 링크)
    cnt = 0
    driver.get(taobao_url)

    for item in shop_items:
        image_path = save_image_and_return_abs_path(item.item_image_url)
        if image_path:
            taobao_item_link, taobao_image_link = taobao_search.taobao_image_search(driver, image_path)
            print(cnt + 1)
            item.item_taobao_item_url = taobao_item_link
            item.item_taobao_image_url = taobao_image_link
        cnt += 1
        time.sleep(3)

    # todo: 배송비 측정

    print('close webDriver')
    SingletonWebDriver.close_driver()
    return keywordlist


if __name__ == '__main__':
    app.run()
