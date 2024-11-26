import subprocess
import time


def open_chrome():
    try:
        chrome_process = subprocess.Popen([
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            '--remote-debugging-port=9222',
            '--user-data-dir=C:\\temp-remote-debug',
            '--incognito',
            '--allow-running-insecure-content',
            '--window-size=800,680',
            'https://www.auction.co.kr/'
        ])
        time.sleep(2)
        print('Chrome has been opened successfully.')
        return chrome_process
    except Exception as e:
        print(f"Failed to open Chrome: {e}")


def close_chrome(chrome_process):
    # 크롬 프로세스 닫기
    chrome_process.terminate()  # 프로세스 소프트웨어 종료
    chrome_process.wait()  # 프로세스가 종료될 때까지 대기