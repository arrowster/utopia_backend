import re


def keyword_search(item_name):
    # 전처리
    item_name = re.sub(r'[a-zA-Z0-9]', '', item_name)
    item_name = re.sub(r'\W+', ' ', item_name)
    words = item_name.split()

    words

    return words
