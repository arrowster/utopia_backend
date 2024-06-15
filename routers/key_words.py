from flask import request

keywordList = []


def key_words():
    keywords = request.args.get('keywords')

    keywordList.append(keywords.split(','))

    return keywordList
