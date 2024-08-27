import time

from flask import Flask, jsonify
from dataclasses import asdict
from routers import routers
from utills.SingletonWebDriver import SingletonWebDriver
from utills.save_image_and_return_abs_path import save_image_and_return_abs_path
from utills.print_running_time import print_running_time
from utills.convert_sets_to_lists import convert_sets_to_lists
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
    max_cnt_item = 50 # todo: 이것도 사용자에게 받아야함 생략 불가 단위 50
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
    start_time = time.localtime()
    print(f'수집 시작 시간: {start_time.tm_hour}:{start_time.tm_min}:{start_time.tm_sec}')

    # 마켓 검색
    shop_list = market_search.gmarket_search(driver, keywordlist)
    print(shop_list)
    print(f'{len(shop_list)}개의 마켓을 찾음')

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

    if max_cnt_item > len(shop_items): #
        all_item_cnt = len(shop_items)
    else:
        all_item_cnt = max_cnt_item

    # 타오바오 링크, 타오바오 이미지 수집
    for item in shop_items:
        image_path = save_image_and_return_abs_path(item.item_image_url)
        if image_path:
            taobao_item = taobao_search.taobao_image_search(driver, image_path)
            if taobao_item:
                taobao_item_link, taobao_image_link = taobao_item
            else:
                continue

            print(f'{cnt + 1} / {all_item_cnt}')
            item.item_taobao_item_url = taobao_item_link
            item.item_taobao_image_url = taobao_image_link
        cnt += 1
        if cnt >= max_cnt_item:
            break
        time.sleep(2)

    print(f'누락 {all_item_cnt - cnt}개') # 최대수 따로 뽑아서 해야함
    print(shop_items)

    end_time = time.localtime()
    print(f'수집 종료 시간: {end_time.tm_hour}:{end_time.tm_min}:{end_time.tm_sec}')
    SingletonWebDriver.close_driver()

    print_running_time(start_time, end_time)
    print(f'수집 아이템 수: {cnt}개')

    shop_items_dict = [asdict(item) for item in shop_items]
    shop_items_list = convert_sets_to_lists(shop_items_dict)
    print('done.')
    return jsonify(shop_items_list)


if __name__ == '__main__':
    app.run()
