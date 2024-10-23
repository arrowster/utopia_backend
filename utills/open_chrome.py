import subprocess
import time


def open_chrome():
    chrome_process = subprocess.Popen([
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        '--remote-debugging-port=9222',  # 디버깅 포트
        '--user-data-dir=C:\\Temp',  # 사용자 데이터 디렉터리
        '--incognito',  # 시크릿 모드
        '--ignore-certificate-errors',  # http 접속 오류 방지
        '--allow-running-insecure-content',  # 안전하지 않은 콘텐츠 허용
        '--window-size=800,680',  # 창 크기
        'https://www.auction.co.kr/'
    ])
    time.sleep(2)
    return chrome_process


def close_chrome(chrome_process):
    # 크롬 프로세스 닫기
    chrome_process.terminate()  # 프로세스 소프트웨어 종료
    chrome_process.wait()  # 프로세스가 종료될 때까지 대기
