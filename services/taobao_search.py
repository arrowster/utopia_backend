import time
from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def taobao_login(driver):
    url = ('https://login.taobao.com/member/login.jhtml?spm=a21n57.1.754894437.1.491d523cCRi6o6&f=top&redirectURL'
           '=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3D%26type%3Dp%26tmhkh5%3D%26from%3Dsea_1_searchbutton%26catId'
           '%3D100%26spm%3Da2141.241046-kr.searchbar.d_2_searchbox')
    driver.get(url)

    try:
        WebDriverWait(driver, 120).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="J_SiteNavLogin"]/div[1]'))
        )
        print("로그인 성공")

    except Exception as e:
        Exception("로그인 실패 또는 시간 초과: ", e)


def taobao_image_search(driver, img_path):
    try:
        upload_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        search_button = driver.find_element(By.ID, 'image-search-upload-button')
        upload_input.send_keys(img_path)
        time.sleep(1)
        search_button.click()
    except Exception as e:
        print("err:", e)
        return False

    try:
        load_position = '//*[@id="pageContent"]/div[1]/div[2]/div/div/a[1]'
        WebDriverWait(driver, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, load_position))
        )
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        search_item = soup.select_one('a[class^="ImgSearchCard--doubleCardWrapper--"]')

        if search_item:
            try:
                item_url = search_item['href']
            except KeyError:
                print("타오바오 아이템 URL 서치 실패")
                item_url = None

            try:
                image_tag = search_item.select_one('div[class^="MainPic--mainPicWrapper--"] img')
                image_url = image_tag['src'] if image_tag else None
            except KeyError:
                print("타오바오 이미지 서치 실패")
                image_url = None

            if item_url and image_url:
                taobao_item_info = [item_url, image_url]
                return taobao_item_info
            else:
                print("필수 정보를 모두 찾지 못했습니다.")
                return False
        else:
            print("검색 아이템을 찾을 수 없습니다.")
            return False

    except TimeoutException as e:
        print("time out 페이지 로드 중 오류 발생:", e)
        return False
