import os
import sys
# from __init__ import root_folder_path
# sys.path.append(root_folder_path)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager    

import pandas as pd
import time

# from library.basic import *

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


service = Service(ChromeDriverManager().install())
# 크롬 드라이버 경로 설정
# chrome_default_driver_path = join_folder_path(root_folder_path, 'chromedriver', 'chromedriver.exe')  # 정확한 경로로 변경
# while(True):
#     if not path_exist(chrome_default_driver_path):
#         clear()
#         chrome_default_driver_path = strip_quotes(input("Enter chromedriver.exe path : "))
#     else:
#         break

class Crawling:
    def __init__(self, url) -> None:
        # 크롬 드라이버 서비스 생성
        # self.service = Service(chrome_driver_path)
        # self.driver = webdriver.Chrome(service=self.service)

        # WebDriver Manager를 사용하여 ChromeDriver 설정
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 웹 페이지 열기
        self.set_url(url)
        
    def find_element(self, selector:str, keyword:str):
        select = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "css_selector": By.CSS_SELECTOR
        }
        
        try:
            get_data = self.driver.find_element(select[selector], keyword)
        except:
            return None
        
        return get_data

    def find_elements(self, selector:str, keyword:str):
        select = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "class": By.CLASS_NAME,
            "tag": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
            "css_selector": By.CSS_SELECTOR
        }
        
        try:
            get_data = self.driver.find_elements(select[selector], keyword)
        except:
            return None
        
        return get_data

    def maximize(self):
        self.driver.maximize_window()
    
    def set_url(self, url):
        self.url = url
        return self
    
    def quit(self):
        self.driver.quit()

    def run(self, wait_time=10):
        self.driver.get(self.url)

        # # 페이지 로딩을 기다리기 위해 약간의 지연 시간 추가
        time.sleep(5)  # 5초 동안 대기. 네트워크 상태에 따라 조절 가능

        # # 필요한 데이터가 로드될 때까지 대기
        wait = WebDriverWait(self.driver, wait_time)
        return wait
        # # 테이블 데이터 찾기
        # rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//table/tbody/tr')))
        # data = []
        # [data.append([col.text for col in row.find_elements(By.TAG_NAME, 'td')]) for row in rows]
        # print("=================")
        # # 데이터 프레임 변환 전에 출력해보기
        # print(data)

        try:
            pass
            # # 데이터프레임으로 변환
            # df = pd.DataFrame(data, columns=['index', '도메인', '방문수', '데스크톱 공유', '모바일 공유', 'MoM', 'YoY', '주요 트래픽 소스'])

            # # 데이터프레임 출력
            # print(df)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # 브라우저 닫기
            self.driver.quit()

if __name__ == "__main__":
    # if not os.path.exists(chrome_default_driver_path): chrome_dirver_path = input("Enter chrome_default_driver_path : ").strip("\"")
    # else: chrome_dirver_path = chrome_default_driver_path
    url = 'https://ko.semrush.com/trending-websites/it/apparel-and-fashion'
    obj = Crawling(url=url)
    obj.run()