from flask import request

keywordList = []


def key_words():
    keywords = request.args.get('keywords')
    keywordList.extend(keywords.split(','))

    return keywordList
