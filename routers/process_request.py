from flask import request


def process_request():
    keywords = request.args.get('keywords', '').split(',')
    min_price = request.args.get('minPrice', 0, type=int)
    max_price = request.args.get('maxPrice', 100000000, type=int)
    collect_cnt = request.args.get('collectCnt', 100, type=int)

    return keywords, min_price, max_price, collect_cnt


def xlsx_data_request():
    request_data = request.json
    convert_type_code = request_data.get('convertCode')
    data = request_data.get('data', [])
    return convert_type_code, data
