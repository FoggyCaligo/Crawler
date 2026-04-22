from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import selenium.webdriver
import re
import time
import random

class Crawler:
  def __init__(self):
    #셀레늄 초기화
    chrome_options = Options()
    #브라우저창 보이게 하는 옵션
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    self.driver = webdriver.Chrome(options=chrome_options)
    self.target_url = "https://www.10000recipe.com/recipe/list.html"
    self.driver.get(self.target_url)
    
    self.speed = {
      'super slow' : 2.0,
      'slow': 1.0,
      'normal':0.5,
      'fast':0.1,
      'super fast':0.05,
    }
  
  def wait(self,a=0.1, b=0.2):
        a = self.speed['super slow']
        b = self.speed['super slow']+0.05
        # 0.1~1.0 사이의 랜덤 대기 시간
        random_wait = random.uniform(a, b)
        time.sleep(random_wait)
  
  def get_elem_xpath(self,xpath):
        return self.driver.find_element(By.XPATH, xpath)
  # click : elem.click

  def back(self, wait_a = 0, wait_b = 0):
        self.driver.back()
        if wait_a != 0 and wait_b != 0:
            self.wait(wait_a, wait_b)

  def click(self,elem, wait_a = 0, wait_b = 0):
        # 광고/고정영역에 가려지는 클릭 충돌을 줄이기 위해 중앙으로 스크롤 후 클릭
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            elem,
        )
        try:
            elem.click()
        except ElementClickInterceptedException:
            # 최후 수단: JS 클릭 (겹침 이슈 우회)
            self.driver.execute_script("arguments[0].click();", elem)
        if wait_a != 0 and wait_b != 0:
            self.wait(wait_a, wait_b)

  def type(self,elem,text, wait_a = 0, wait_b = 0):
        elem.send_keys(text)
        if wait_a != 0 and wait_b != 0:
            self.wait(wait_a, wait_b)

  def download(self,elem, wait_a = 0, wait_b = 0):
        if wait_a != 0 and wait_b != 0:
            self.wait(wait_a, wait_b)
        return elem.screenshot(f"./resultGraph.png")
