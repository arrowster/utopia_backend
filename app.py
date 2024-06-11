from flask import Flask

from routers.test_signal import test_signal

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/test-signal')
def test_sig():
    return test_signal()


@app.route('/market-search')
def market_search():
    #todo: keyword get
    #todo: naver 마켓 수집
    #todo: keyword 가지치기
    #todo: 배송비 측정
    return 'search'


if __name__ == '__main__':
    app.run()
