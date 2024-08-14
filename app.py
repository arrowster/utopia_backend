import time

from flask import Flask
from routers import routers
from utills.SingletonWebDriver import SingletonWebDriver
from utills.save_image_and_return_abs_path import save_image_and_return_abs_path
from services import market_search
from services import taobao_search
from services.pruning_shop_item import pruning_shop_item, search_seb_keywords

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

    # 아이템 가지 치기 (아이템 이름, 이미지, 네이버 카테고리, 메인 키워드 수집)
    shop_items = pruning_shop_item(driver, shop_list, min_price, max_price)
    print(f'{shop_items},\r\n'
          f'{len(shop_items)}개')

    # 서브 키워드 수집
    main_keyword_to_sub_keywords = {}

    for item in shop_items:
        main_keyword = item.item_main_keywords
        if main_keyword not in main_keyword_to_sub_keywords:
            sub_keywords = search_seb_keywords(driver, main_keyword)
            main_keyword_to_sub_keywords[main_keyword] = sub_keywords
        else:
            sub_keywords = main_keyword_to_sub_keywords[main_keyword]

        item.item_sub_keywords = sub_keywords

    # todo: 트래픽 이슈 해결 필
    cnt = 0
    driver.get(taobao_url)

    # 타오바오 링크, 타오바오 이미지 수집
    for item in shop_items:
        image_path = save_image_and_return_abs_path(item.item_image_url)
        if image_path:
            taobao_item = taobao_search.taobao_image_search(driver, image_path)
            if taobao_item:
                taobao_item_link, taobao_image_link = taobao_item
            else:
                continue

            print(f'{cnt + 1} / {len(shop_items)}')
            item.item_taobao_item_url = taobao_item_link
            item.item_taobao_image_url = taobao_image_link
        cnt += 1
        time.sleep(2)
    print(f'누락 {len(shop_items) - cnt}개')
    print(shop_items)

    print('close webDriver')
    SingletonWebDriver.close_driver()
    return keywordlist


if __name__ == '__main__':
    app.run()
