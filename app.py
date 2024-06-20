from flask import Flask
from routers import routers
from controllers import gmarket_search

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
    gmarket_search.gmarket_search(keywordlist)
    #todo: keyword get
    #todo: naver 마켓 수집
    #todo: keyword 가지치기
    #todo: 배송비 측정
    return keywordlist


if __name__ == '__main__':
    app.run()
