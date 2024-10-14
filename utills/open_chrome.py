import subprocess
import time


def open_chrome():
    subprocess.Popen([
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        '--remote-debugging-port=9222',  # 디버깅 포트
        '--user-data-dir=C:\\Temp',  # 사용자 데이터 디렉터리
        '--incognito',  # 시크릿 모드
        '--ignore-certificate-errors'  # http 접속 오류 방지
        '--window-size=800,680',  # 창 크기
        'https://www.auction.co.kr/'  # 열고자 하는 URL
    ])
    time.sleep(2)
