import random
import time

from models.ShopItem import ShopItem
from utills.SingletonWebDriver import get_soup_from_url, get_soup_wait_class_element
from utills.keyword_split import keyword_split


def pruning_shop_item(driver, shop_list, min_price, max_price, platform):
    items = []
    sold_item_keywords = set()
    for shop_url in shop_list:
        if platform == 'auction':
            keywords = sold_item_keyword_at_auction(driver, shop_url, min_price, max_price)
        elif platform == 'gmarket':
            keywords = sold_item_keyword_at_gmarket(driver, shop_url, min_price, max_price)
        else:
            raise ValueError(f"Invalid platform: {platform}. Use 'gmarket' or 'auction'.")

        if not keywords:
            continue
        sold_item_keywords.update(keywords)
    print(sold_item_keywords)

    for item_keyword in sold_item_keywords:
        item = pruning_naver_shoping(driver, item_keyword)
        if item:
            items.extend(item)

    return items


def sold_item_keyword_at_auction(driver, url, min_price, max_price):
    sold_item_keywords = []

    add_url = ('/List?Title=Best%20Item&CategoryType=General&SortType=MostPopular&DisplayType=List&Page=0&PageIndex=0'
               '&PageSize=10&IsFreeShipping=False&Is3PL=False')
    price_url = f'&minPrice={min_price}&maxPrice={max_price}' if min_price or max_price else ''
    shop_url = url + add_url + price_url
    soup = get_soup_from_url(driver, shop_url)
    if not soup:
        return False

    try:
        first_li = soup.select_one('#ulCategory > li:nth-child(1)')
    except Exception as e:
        print('not found : ', e)
        return False

    first_li_name = first_li.find('a').text

    # '공구/안전/산업용품' 카테고리 확인
    if first_li_name == '공구/안전/산업용품':
        all_shop_item = soup.find('tbody').find_all('tr')
        for item in all_shop_item:
            item_link = item.find('a')

            if item_link and 'href' in item_link.attrs:
                item_link_url = item_link['href']
                time.sleep(random.randint(2, 5))
                item_soup = get_soup_wait_class_element(driver, item_link_url, 'buy_num', False)

                if item_soup:
                    item_name_tag = item_soup.find('h1', {'class': 'itemtit'})

                    if item_name_tag:
                        item_name = item_name_tag.text.strip()
                        keywords = keyword_split(item_name)
                        item_main_keywords = ' '.join(keywords[:3])
                        sold_item_keywords.append(item_main_keywords)
                        print(item_name)
                else:
                    break
    else:
        return False

    return sold_item_keywords


def sold_item_keyword_at_gmarket(driver, url, min_price, max_price):
    sold_item_keywords = []
    add_url = ('/List?keyword=&category=&title=Best+Item&sortType=MostPopular&displayType=List&page=1&pageSize=60'
               '&isFreeShipping=false&hasDiscount=false&isInternationalShipping=false'
               '&isTpl=false')
    price_url = f'&minPrice={min_price}&maxPrice={max_price}' if min_price or max_price else ''
    shop_url = url + add_url + price_url
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
                    keywords = keyword_split(name_tag)
                    item_main_keywords = ' '.join(keywords[:3])
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
        img_tag = item.select_one("div[class^='product_img_area__']").find('img')
        if img_tag:
            product_image_url = img_tag['src']
        else:
            print(f"이미지 서치 실패: {url}, {pruning_item_name}")
            continue

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
            items.append(
                ShopItem(
                    item_name=product_item_name,
                    item_image_url=product_image_url,
                    item_naver_category=product_category,
                    item_main_keywords=pruning_item_name
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


def search_seb_keywords(driver, main_keyword):
    sub_keywords = set()
    # todo: 네이버 쇼핑에서 20개 리스트 뽑아서 메인키워드 제외하고, 중복되지 않게 넣어야 함
    url = f'https://search.shopping.naver.com/search/all?pagingIndex=1&pagingSize=20&productSet=total&query={main_keyword}&sort=rel&timestamp=&viewType=list'
    # 메인 키워드 분리
    main_keywords = keyword_split(main_keyword)

    soup = get_soup_from_url(driver, url)

    product_item = soup.select("div[class^='product_item__']")

    for item in product_item:
        name_tag = item.select_one("div[class^='product_title__']").find('a').text
        product_item_name = name_tag if name_tag else None
        keywords = keyword_split(product_item_name)
        sub_keywords.update(keywords)

    for keyword in main_keywords:
        sub_keywords.discard(keyword)

    return sub_keywords
