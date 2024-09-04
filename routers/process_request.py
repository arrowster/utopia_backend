from flask import request

def process_request():
    # 키워드 처리
    keyword_list = []
    keywords = request.args.get('keywords')
    if keywords:
        keyword_list.extend(keywords.split(','))

    # 수집 환경 처리
    env = {
        'min': request.args.get('min', type=int),
        'max': request.args.get('max', type=int),
        'cnt': request.args.get('cnt', type=int)
    }

    return keyword_list, env
