import os
import requests
import re
from datetime import datetime
from PIL import Image
from io import BytesIO


def save_image_and_return_abs_path(url):
    pattern = re.compile(r"https:\/\/shopping-phinf\.pstatic\.net\/main_\d+\/\d+(\.\d+)?\.jpg\?type=f140")
    os.makedirs('./temp_img', exist_ok=True)

    match = pattern.match(url)
    if not match:
        print(f"dont match: {url}")

    time = datetime.now().strftime("%d%H%M%S%f")
    path = f'./temp_img/{time}.JPEG'
    flag = download_image(url, path)
    file_abs_path = os.path.abspath(path)
    if flag:
        return file_abs_path
    else:
        return False


def download_image(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        try:
            img = Image.open(BytesIO(response.content))
            img.save(path, 'JPEG')
            return True
        except Exception as e:
            print(f'이미지를 JPEG로 저장을 실패했습니다: {url}, 오류: {e}')
            return False
    else:
        print(f'이미지를 다운로드를 실패했습니다: {url}')
        return False
