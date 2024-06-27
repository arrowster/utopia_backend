from flask import request


def key_words():
    keyword_list = []
    keywords = request.args.get('keywords')
    keyword_list.extend(keywords.split(','))

    return keyword_list
