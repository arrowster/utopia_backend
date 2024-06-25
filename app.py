from flask import Flask
from routers import routers
from controllers.gmarket_search import gmarket_search
from controllers.pruning_shop_item import pruning_shop_item
from controllers.download_image import download_image

import os

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/test-signal')
def test_sig_func():
    return routers.test_signal()


@app.route('/market-search')
def market_search_func():
    keywordlist = routers.key_words()
    print(keywordlist)
    shop_list = gmarket_search(keywordlist)
    print(shop_list)
    shop_item_urls = pruning_shop_item(shop_list)
    print(shop_item_urls)

    os.makedirs('./temp_img', exist_ok=True)
    count_img = 0
    count_fail_img = 0
    for url in shop_item_urls:
        flag = download_image(url, f'./temp_img/{ count_img }.jpg')
        if flag:
            count_img += 1
        else:
            count_fail_img += 1
    print(f'image 추출이 완료됨 총 { count_img }개, 누락 { count_fail_img }')

    #todo: keyword 가지치기
    # url 이미지 다운로드
    # taobao 이미지 검색
    # url 3개 씩 뽑아오기
    #todo: 배송비 측정
    return keywordlist


if __name__ == '__main__':
    app.run()
