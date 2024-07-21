from flask import Flask
from routers import routers
from utills.SingletonWebDriver import SingletonWebDriver
from utills.save_urls_image_in_directory import save_urls_image_in_directory
from services import market_search
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
    min_price = None  # todo: 이것도 사용자에게 받아야함 생략 가능
    max_price = None

    keywordlist = routers.key_words()
    print(keywordlist)

    # todo: web띄워서 타오바오 로그인 url 보여주기
    # 로그인 완료 서버에 알려줘야함...

    shop_list = market_search.gmarket_search(driver, keywordlist)
    print(shop_list)
    shop_items = pruning_shop_item(driver, shop_list, min_price, max_price)
    print(f'{shop_items},\r\n'
          f'{len(shop_items)}개')

    image_urls = [item.item_image_url for item in shop_items]
    save_images_id = save_urls_image_in_directory(image_urls)

    # todo: 타오바오 이미지 검색 및 요소 가져와야함

    # todo: 배송비 측정

    print('close webDriver')
    SingletonWebDriver.close_driver()
    return keywordlist


if __name__ == '__main__':
    app.run()
