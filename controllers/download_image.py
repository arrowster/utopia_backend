import requests


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
