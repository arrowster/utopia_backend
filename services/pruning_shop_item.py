from utopia_backend.models.ShopItem import ShopItem
from utopia_backend.utills.SingletonWebDriver import get_soup_from_url
from utopia_backend.utills.keyword_search import keyword_search


def pruning_shop_item(driver, shop_list, min_price, max_price):
    items = []
    sold_item_keywords = []
    for shop_url in shop_list:
        #todo:나중에 쇼핑물 별로 분류 필요

        keywords = sold_item_keyword_at_gmarket(driver, shop_url, min_price, max_price)
        if not keywords:
            continue
        sold_item_keywords.extend(keywords)

    for item_keyword in sold_item_keywords:
        item = pruning_naver_shoping(driver, item_keyword)
        if item:
            items.extend(item)

    return items


def sold_item_keyword_at_gmarket(driver, url, min_price, max_price):
    sold_item_keywords = []
    add_url = ('/List?keyword=&category=&title=Best+Item&sortType=MostPopular&displayType=List&page=1&pageSize=60'
               '&isFreeShipping=false&hasDiscount=false&isInternationalShipping=false'
               '&isTpl=false')
    price_url = f'&minPrice={min_price}&maxPrice={max_price}'
    https = 'https:'

    if max_price:
        print(max_price)
        shop_url = url + add_url + price_url
    else:
        shop_url = url + add_url
    soup = get_soup_from_url(driver, shop_url)

    first_li = soup.select_one('#ulCategory > li:nth-child(1)')
    first_li_name = first_li.find('a').text

    if first_li_name == '공구/안전/산업용품':
        all_shop_item = soup.find_all('tr')
        for item in all_shop_item:
            review_span = item.find('span', {'class': 'cnt'})
            if review_span:
                name_tag = item.find('p', {'class': 'sbj'}).find('a').text
                if name_tag:
                    item_main_keywords = keyword_search(name_tag)
                    print(item_main_keywords)
                    sold_item_keywords.append(item_main_keywords)
    else:
        return False
    return sold_item_keywords


def pruning_naver_shoping(driver, pruning_item_name):
    items = []
    url = ('https://search.shopping.naver.com/search/all?pagingIndex=1&pagingSize=3&productSet=overseas&'
           f'query={pruning_item_name}&sort=rel&timestamp=&viewType=list')

    soup = get_soup_from_url(driver, url)

    product_item = soup.select("div[class^='product_item__']")
    product_items = product_item[:3]

    prev_category = None
    for item in product_items:
        # 제품 이미지 URL 추출
        img_tag = item.find('img')
        product_image_url = img_tag['src'] if img_tag else None

        # 제품 이름 추출
        name_tag = item.select_one("div[class^='product_title__']").find('a').text
        product_item_name = name_tag if name_tag else None

        # 제품 카테고리 추출
        category_tag = item.select_one("div[class^='product_depth__']")
        categories = [span.get_text(strip=True) for span in category_tag.find_all('span')] if category_tag else None
        product_category = ' > '.join(categories)

        if prev_category is None:
            prev_category = product_category

        if check_category_identities(prev_category, product_category):
            print(product_item_name)
            print(product_image_url)
            print(product_category)
            items.append(
                ShopItem(
                    item_name=product_item_name,
                    item_image_url=product_image_url,
                    item_naver_category=product_category
                )
            )
        else:
            return False

    return items


def check_category_identities(criteria, target):
    if criteria == target:
        return True
    else:
        return False
