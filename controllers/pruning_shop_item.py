from utopia_backend.controllers.SingletonWebDriver import get_soup_from_url


def pruning_shop_item(driver, shop_list):
    img_urls = []
    for shop_url in shop_list:
        #todo:나중에 쇼핑물 별로 분류 필요

        img_url = pruning_gmarket_item(driver, shop_url)
        if not img_url:
            continue
        img_urls.extend(img_url)

    return img_urls


def pruning_gmarket_item(driver, url):
    img_urls = []
    add_url = ('/List?Title=Best%20Item&CategoryType=General&SortType=FocusRank&DisplayType=List&Page=1&PageSize=60'
               '&IsFreeShipping=False&HasDiscount=False&HasStamp=False&HasMileage=False&IsInternationalShipping=False'
               '&IsTpl=False&Roles=System.String%5B%5D&NeedToGetSDBrandName=True#listTop')
    https = 'https:'

    shop_url = url + add_url
    soup = get_soup_from_url(driver, shop_url)

    first_li = soup.select_one('#ulCategory > li:nth-child(1)')
    first_li_name = first_li.find('a').text

    if first_li_name == '공구/안전/산업용품':
        all_shop_item = soup.find_all('tr')
        for item in all_shop_item:
            review_span = item.find('span', {'class': 'cnt'})
            if review_span:
                img_tag = item.find('p', {'class': 'img'}).find('img')
                if img_tag and 'data-original' in img_tag.attrs:
                    img_urls.append(https + img_tag['data-original'])
    else:
        return False
    return img_urls
