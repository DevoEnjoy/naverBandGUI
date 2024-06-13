import os
import sys
from __init__ import root_folder_path
sys.path.append(root_folder_path)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

from library.basic import *

# 크롬 드라이버 경로 설정
chrome_default_driver_path = join_folder_path(root_folder_path, 'chromedriver', 'chromedriver.exe')  # 정확한 경로로 변경
while(True):
    if not path_exist(chrome_default_driver_path):
        clear()
        chrome_default_driver_path = strip_quotes(input("Enter chromedriver.exe path : "))
    else:
        break

class Crawling:

    def __init__(self, url, chrome_driver_path=chrome_default_driver_path) -> None:
        # 크롬 드라이버 서비스 생성
        self.service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service)


        # 웹 페이지 열기
        self.url = url

    def run(self):
        self.driver.get(self.url)

        # 페이지 로딩을 기다리기 위해 약간의 지연 시간 추가
        time.sleep(5)  # 5초 동안 대기. 네트워크 상태에 따라 조절 가능

        # 필요한 데이터가 로드될 때까지 대기
        wait = WebDriverWait(self.driver, 10)

        # 테이블 데이터 찾기
        rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr')))
        data = []
        [data.append([col.text for col in row.find_elements(By.TAG_NAME, 'td')]) for row in rows]
        print("=================")
        # 데이터 프레임 변환 전에 출력해보기
        print(data)

        try:
            # 데이터프레임으로 변환
            df = pd.DataFrame(data, columns=['index', '도메인', '방문수', '데스크톱 공유', '모바일 공유', 'MoM', 'YoY', '주요 트래픽 소스'])

            # 데이터프레임 출력
            print(df)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # 브라우저 닫기
            self.driver.quit()

if __name__ == "__main__":
    if not os.path.exists(chrome_default_driver_path):
        chrome_dirver_path = input("Enter chrome_default_driver_path : ").strip("\"")
    else:
        chrome_dirver_path = chrome_default_driver_path
    url = 'https://ko.semrush.com/trending-websites/it/apparel-and-fashion'
    obj = Crawling(url=url, chrome_driver_path=chrome_dirver_path)
    obj.run()