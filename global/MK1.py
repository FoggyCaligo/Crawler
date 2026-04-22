from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver
import csv
import pytesseract
# import easyocr
import csv
import re
import time
import random

#img2text in list format
# def img2list():
#     image_path = 'resultGraph.png'  # 또는 절대 경로 지정
#     # EasyOCR Reader 객체 생성 (한국어 + 영어)
#     reader = easyocr.Reader(['ko', 'en'])

#     # 이미지에서 텍스트 인식
#     results = reader.readtext(image_path)
#     # 정규식: "숫자 + 원 또는 유사문자"
#     pattern = r'([\d,\.]+)\s*[원왼완읜윈웡웞웟!웟욋왓읫]+'
#     # 결과 파싱
#     matched_values = []
#     for bbox, text, conf in results:
#         matches = re.findall(pattern, text)
#         for m in matches:
#             clean_number = m.replace(',', '').replace('.', '')
#             matched_values.append(clean_number)
#     return matched_values

#data save class
class CSV:
    def __init__(self, filename="result.csv"):
        self.filename = filename
        self.file = open(filename, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["진단명","석션피딩","치매섬망수면장애","마비욕창","전염성질환", "minPrice", "price", "maxPrice",'stdDate'])

    def write(self,disease,Q1,Q2,Q3,Q4,minPrice,price,maxPrice,stdDate):
        self.filename = "./result.csv"
        self.file = open("./result.csv", "a", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        self.writer.writerow([disease,Q1,Q2,Q3,Q4,minPrice,price,maxPrice,stdDate])

    def __del__(self):
        self.file.close()

#main crawler   
class Crawler:
    def __init__(self):
        self.csv = CSV()
        #셀레늄 초기화
        chrome_options = Options()
        #브라우저창 보이게 하는 옵션
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
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

        self.page1_elems = {
           "recipe_type" : "/html/body/dl/dd/div[1]/table/tbody/tr[1]/td/div/div[1]",
           "recipe_list" : "/html/body/dl/dd/ul/ul",
        }

        self.elements = {
            "page1_recipe_type" : "/html/body/dl/dd/div[1]/table/tbody/tr[1]/td/div/div[1]",
            "page1_recipe_list" : "/html/body/dl/dd/ul/ul",

        }
    
    #basic functions
    def access_url(self):
        #셀레늄 초기화
        chrome_options = Options()
        #브라우저창 보이게 하는 옵션
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.target_url = "https://www.10000recipe.com/recipe/list.html"
        self.driver.get(self.target_url)
        self.driver.get(self.target_url)

    def wait(self,a=0.1, b=0.2):
        a = self.speed['super fast']
        b = self.speed['super fast']+0.05
        # 0.1~1.0 사이의 랜덤 대기 시간
        random_wait = random.uniform(a, b)
        time.sleep(random_wait)
    #operating functions
    def get_element(self,name,extra=""):
        try:
            return self.driver.find_element(By.XPATH, self.elements[name]+extra)
        except:
            return self.driver.find_element(By.XPATH, self.elements[name]+extra)
    
    def get_elem_xpath(self,xpath):
            return self.driver.find_element(By.XPATH, xpath)
    
    def back(self):
        self.driver.back()
        self.wait()
    
    def click(self,name, wait=True):
        try:
            self.get_element(name).click()
        except:
            self.get_element(name).click()
        if wait==True:
            self.wait()

    def type(self,name,text):
        try:
            self.get_element(name).send_keys(text)
        except:
            self.get_element(name).send_keys(text)
        self.wait()
    def download(self,name):
        try:
            return self.get_element(name).screenshot(f"./resultGraph.png")
        except:
            return self.get_element(name).screenshot(f"./resultGraph.png")




            
    #main process function
    def main(self):
        #접속
        self.access_url()
        pytesseract.pytesseract.tesseract_cmd = r'./tesseract-ocr.exe'
        
        # self.click(self.page1_elems["recipe_type"]+"/li[{1}]")
        
        for i in range(self.get_element("page1_recipe_list").__sizeof__()):
            self.wait(2.0,3.0)
            self.click(self.get_element(self.page1_elems["recipe_list"]+f"/li[{i+1}]"))
            self.wait(0.5,1.0)
            self.back()



crawler = Crawler()
crawler.main()