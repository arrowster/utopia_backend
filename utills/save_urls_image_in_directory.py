import os
import requests
import re


def save_urls_image_in_directory(urls):
    pattern = re.compile(r"https:\/\/shopping-phinf\.pstatic\.net\/main_\d+\/\d+(\.\d+)?\.jpg\?type=f140")
    os.makedirs('./temp_img', exist_ok=True)
    count_img = 0
    count_fail_img = 0
    image_names = []

    for url in urls:
        match = pattern.match(url)
        if not match:
            count_fail_img += 1
            print(f"dont match: {url}")
            continue

        item_number = count_img
        flag = download_image(url, f'./temp_img/{ item_number }.jpg')
        if flag:
            count_img += 1
            image_names.append(item_number)
        else:
            count_fail_img += 1
    print(f'image 추출이 완료됨 총 { count_img }개, 누락 { count_fail_img }')
    return image_names


def download_image(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        return True
    else:
        print(f'Failed to download image: {url}')

        return False
