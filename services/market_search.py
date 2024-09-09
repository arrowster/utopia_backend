from utills.SingletonWebDriver import get_soup_from_url


def search_shops(driver, words, platform):
    search_data = {
        'gmarket': {
            'url_template': 'https://www.gmarket.co.kr/n/search?keyword={word}&f=o:i&k=0&p=1&v=l',
            'shop_class': 'link__shop'
        },
        'auction': {
            'url_template': 'https://www.auction.co.kr/n/search?keyword={word}',
            'shop_class': 'link--shop'
        }
    }

    if platform not in search_data:
        raise ValueError(f"Invalid platform: {platform}. Use 'gmarket' or 'auction'.")

    shop_set = set()

    # 마켓 수집
    for word in words:
        url = search_data[platform]['url_template'].format(word=word)
        soup = get_soup_from_url(driver, url)
        product_items = soup.find_all('a', class_=search_data[platform]['shop_class'])

        for item in product_items:
            if item and 'href' in item.attrs:
                shop_url = item['href']
                shop_set.add(shop_url)
            else:
                print("가게 링크를 찾을 수 없습니다.")

    return list(shop_set)
