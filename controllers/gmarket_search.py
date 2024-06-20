from utopia_backend.controllers.driver import initialize_driver, get_soup_from_url


def gmarket_search(words):
    driver = initialize_driver()

    for word in words:
        shop_set = set()
        url = f'https://www.gmarket.co.kr/n/search?keyword={word}&f=o:i&k=0&p=1&v=l'
        soup = get_soup_from_url(driver, url)
        product_items = soup.find_all('a', class_='link__shop')
        print(product_items)

        for item in product_items:
            if item and 'href' in item.attrs:
                shop_url = item['href']
                shop_set.add(shop_url)
            else:
                print("가게 링크를 찾을 수 없습니다.")

    driver.quit()
    shop_list = list(shop_set)
    print(shop_list)
    return shop_list
