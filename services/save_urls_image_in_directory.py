import os
import requests


def save_urls_image_in_directory(urls):
    os.makedirs('./temp_img', exist_ok=True)
    count_img = 0
    count_fail_img = 0
    for url in urls:
        flag = download_image(url, f'./temp_img/{ count_img }.jpg')
    if flag:
        count_img += 1
    else:
        count_fail_img += 1
    print(f'image 추출이 완료됨 총 { count_img }개, 누락 { count_fail_img }')
    return 0


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
