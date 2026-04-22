from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver
import cv2
import pytesseract
import easyocr
import csv
import re
import time
import random

#img2text in list format
def img2list():
    image_path = 'resultGraph.png'  # 또는 절대 경로 지정
    # EasyOCR Reader 객체 생성 (한국어 + 영어)
    reader = easyocr.Reader(['ko', 'en'])

    # 이미지에서 텍스트 인식
    results = reader.readtext(image_path)
    # 정규식: "숫자 + 원 또는 유사문자"
    pattern = r'([\d,\.]+)\s*[원왼완읜윈웡웞웟!웟욋왓읫]+'
    # 결과 파싱
    matched_values = []
    for bbox, text, conf in results:
        matches = re.findall(pattern, text)
        for m in matches:
            clean_number = m.replace(',', '').replace('.', '')
            matched_values.append(clean_number)
    return matched_values

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
        self.target_url = "https://www.carenation.kr/service/precalc"
        self.driver.get(self.target_url)
        #질병 종류
        # self.diseases = ["CRE","VRE","간경변","간경화","간농양","간성혼수","간암","간염","간이식","간질","갈비뼈골절","감기","감염","갑상선암","개두술","거동불가","거동불편","검사","결석","결핵","경련","경막하출혈","경추골절","경추손상","고관절골절","고관절수술","고열","고혈압","골반골절","골수염","골수종","골절","공여","관상동맥","관장","관절염","괴사","교모세포종","교정","교통사고","구강암","구토","궤양","기능저하","기력저하","기형","기흉","길랑바레","깁스","낙상","난소암","난청","낭종","내과","내시경","노환","농양","뇌경색","뇌내출혈","뇌동맥류","뇌병변","뇌손상","뇌수막염","뇌수막종","뇌염","뇌전증","뇌졸중","뇌종양","뇌진탕","뇌출혈","뇌하수체종양","다리골절","다발골수종","다발성근육염","담관암","담낭암","담낭염","담도암","담석","당뇨","당뇨합병증","대동맥류","대동맥박리","대동맥판막","대장암","대퇴골두무혈성괴사","대퇴부골절","동맥류","두경부암","디스크","디스크수술","디스크파열","루게릭","루게릭병","류마티스","림프암","림프종","마비","만성폐쇄성폐질환","말기암","망상","모야모야","목디스크","무릎관절수술","무릎수술","무릎연골수술","무릎인공관절수술","무지외반증","물리치료","물혹","발목골절","발목수술","방광암","방광염","백내장","백혈병","변비","복강경","복막염","복수","봉합","부상","부인과","부작용","부정맥","부종","분만","비뇨기과","빈혈","사지마비","상세불명","상해","색전술","석션","선종","설사","설암","섬망","소뇌위축","소변줄","손목골절","손상","쇠약","쇼크","수두증","수면장애","수술","스텐트","시각장애","식도암","식물인간","신경손상","신경외과","신부전","신우신염","신장결석","신장암","신장이식","신장질환","실금","심근경색","심부전","심장질환","심장판막","심정지","심혈관질환","십자인대파열","안과","알츠하이머","양악","어지러움증","어지럼증","언어장애","염좌","염증","옴","와상","외상","외상성뇌출혈","요관암","요로감염","요로결석","요실금","요양","욕창","용종","우울증","위루관","위암","유방암","육종","의식불명","이식","이식수술","이형성증","인공관절","인공관절수술","인대파열","인두암","입원","자궁경부암","자궁근종","자궁내막암","자궁내막증","자궁선근증","자궁암","자궁적출","자상","장루","장애","장염","장폐색","재건술","재활","저산소증","저혈당","저혈압","적출","전립선비대","전립선암","절개","절단","절제","제거","제왕절개","조영술","조직검사","조현병","종양","중풍","중환자","지병","지주막하출혈","지체장애","직장암","척수손상","척수염","척수증","척추골절","척추관협착증","척추손상","척추수술","척추압박골절","척추전방전위증","척추협착","천공","천포창","출산","출혈","췌장암","췌장염","측만","치매","치질","코로나","타박상","탈구","탈수","탈장","탈출","통증","통풍","퇴행성관절염","투석","파열","파킨슨","판막수술","팔골절","패혈증","편마비","폐결핵","폐렴","폐부종","폐색","폐섬유","폐암","폐이식","폐질환","피부암","피부이식","하반신마비","합병증","항암","허리골절","허리디스크","허리디스크수술","허리수술","허리염좌","허리협착증","혈관질환","혈변","혈액암","혈액투석","혈전","협심증","협착","협착증","호흡곤란","호흡기질환","호흡부전","화상","황달","회복","회전근개파열","후두암","후유증","흉수","흡인성폐렴"]
        self.diseases = ["교통사고","구강암","구토","궤양","기능저하","기력저하","기형","기흉","길랑바레","깁스","낙상","난소암","난청","낭종","내과","내시경","노환","농양","뇌경색","뇌내출혈","뇌동맥류","뇌병변","뇌손상","뇌수막염","뇌수막종","뇌염","뇌전증","뇌졸중","뇌종양","뇌진탕","뇌출혈","뇌하수체종양","다리골절","다발골수종","다발성근육염","담관암","담낭암","담낭염","담도암","담석","당뇨","당뇨합병증","대동맥류","대동맥박리","대동맥판막","대장암","대퇴골두무혈성괴사","대퇴부골절","동맥류","두경부암","디스크","디스크수술","디스크파열","루게릭","루게릭병","류마티스","림프암","림프종","마비","만성폐쇄성폐질환","말기암","망상","모야모야","목디스크","무릎관절수술","무릎수술","무릎연골수술","무릎인공관절수술","무지외반증","물리치료","물혹","발목골절","발목수술","방광암","방광염","백내장","백혈병","변비","복강경","복막염","복수","봉합","부상","부인과","부작용","부정맥","부종","분만","비뇨기과","빈혈","사지마비","상세불명","상해","색전술","석션","선종","설사","설암","섬망","소뇌위축","소변줄","손목골절","손상","쇠약","쇼크","수두증","수면장애","수술","스텐트","시각장애","식도암","식물인간","신경손상","신경외과","신부전","신우신염","신장결석","신장암","신장이식","신장질환","실금","심근경색","심부전","심장질환","심장판막","심정지","심혈관질환","십자인대파열","안과","알츠하이머","양악","어지러움증","어지럼증","언어장애","염좌","염증","옴","와상","외상","외상성뇌출혈","요관암","요로감염","요로결석","요실금","요양","욕창","용종","우울증","위루관","위암","유방암","육종","의식불명","이식","이식수술","이형성증","인공관절","인공관절수술","인대파열","인두암","입원","자궁경부암","자궁근종","자궁내막암","자궁내막증","자궁선근증","자궁암","자궁적출","자상","장루","장애","장염","장폐색","재건술","재활","저산소증","저혈당","저혈압","적출","전립선비대","전립선암","절개","절단","절제","제거","제왕절개","조영술","조직검사","조현병","종양","중풍","중환자","지병","지주막하출혈","지체장애","직장암","척수손상","척수염","척수증","척추골절","척추관협착증","척추손상","척추수술","척추압박골절","척추전방전위증","척추협착","천공","천포창","출산","출혈","췌장암","췌장염","측만","치매","치질","코로나","타박상","탈구","탈수","탈장","탈출","통증","통풍","퇴행성관절염","투석","파열","파킨슨","판막수술","팔골절","패혈증","편마비","폐결핵","폐렴","폐부종","폐색","폐섬유","폐암","폐이식","폐질환","피부암","피부이식","하반신마비","합병증","항암","허리골절","허리디스크","허리디스크수술","허리수술","허리염좌","허리협착증","혈관질환","혈변","혈액암","혈액투석","혈전","협심증","협착","협착증","호흡곤란","호흡기질환","호흡부전","화상","황달","회복","회전근개파열","후두암","후유증","흉수","흡인성폐렴"]
        
        
        #사이트 내 요소들
        self.elements = {
            "searchBox": "//*[@id=\"precalcTxt01\"]",
            "deleteBtn": "/html/body/div[1]/main/section/div/article/div/div[1]/button",
            "diseaseList": "//*[@id=\"app\"]/main/section/div/article/div/ul",
            "diseaseItem": "//*[@id=\"app\"]/main/section/div/article/div/ul/li",
            "Q1False" : "//*[@id=\"app\"]/main/section/div/article/div/div[2]/ul/li[1]/div/div/label[1]",
            "Q1True" :  "//*[@id=\"app\"]/main/section/div/article/div/div[2]/ul/li[1]/div/div/label[2]",
            "Q2False" : "//*[@id=\"app\"]/main/section/div/article/div/div[2]/ul/li[2]/div/div/label[1]",
            "Q2True" : "//*[@id=\"app\"]/main/section/div/article/div/div[2]/ul/li[2]/div/div/label[2]",
            "Q3False" : "//*[@id=\"app\"]/main/section/div/article/div/div[2]/ul/li[3]/div/div/label[1]",
            "Q3True" : "//*[@id=\"app\"]/main/section/div/article/div/div[2]/ul/li[3]/div/div/label[2]",
            "Q4False" : "//*[@id=\"app\"]/main/section/div/article/div/div[2]/ul/li[4]/div/div/label[1]",
            "Q4True" : "//*[@id=\"app\"]/main/section/div/article/div/div[2]/ul/li[4]/div/div/label[2]",
            "QCalcResult" : "//*[@id=\"app\"]/main/section/div/article/div/div[2]/div/button",
            "QRetryBtn" : "//*[@id=\"app\"]/main/section/div/article/div[5]/button[2]",
            "graphCanvas" : "//*[@id=\"app\"]/main/section/div/article/div[2]/div[2]/canvas",
            "stdDate" : '//*[@id="app"]/main/section/div/article/div[3]/span',
        }
        #testcases
        self.testcases = [
            [True,True,True,True],
            [True,True,True,False],
            [True,True,False,True],
            [True,True,False,False],
            [True,False,True,True],
        ]
        self.imgPath = "./resultGraph.png"

        self.speed = {
            'super slow' : 2.0,
            'slow': 1.0,
            'normal':0.5,
            'fast':0.1,
            'super fast':0.05,
        }
    #basic functions
    def access_url(self):
        #셀레늄 초기화
        chrome_options = Options()
        #브라우저창 보이게 하는 옵션
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.target_url = "https://www.carenation.kr/service/precalc"
        self.driver.get(self.target_url)
        self.driver.get(self.target_url)

    def wait(self,a=0.1, b=0.2):
        a = self.speed['super slow']
        b = self.speed['super slow']+0.05
        # 0.1~1.0 사이의 랜덤 대기 시간
        random_wait = random.uniform(a, b)
        time.sleep(random_wait)
    #operating functions
    def get_element(self,name):
        try:
            return self.driver.find_element(By.XPATH, self.elements[name])
        except:
            return self.driver.find_element(By.XPATH, self.elements[name])
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

    def graph_to_data(self):
        img = self.download("graphCanvas")
        self.wait()
        img = cv2.imread(f"./resultGraph.png", cv2.IMREAD_GRAYSCALE)
        self.wait()
        return img2list(img)

    #sequance functions
    def search_disease(self,disease):
        #다음 증상 종류 선택 
        try:
            self.click("QRetryBtn")
            self.click("deleteBtn")
        except: 
            pass
        self.click("searchBox")
        self.type("searchBox",disease)
        self.click("diseaseItem")

    def test(self, Q1, Q2, Q3, Q4):
        self.click(Q1==True and "Q1True" or "Q1False", wait=False)
        self.click(Q2==True and "Q2True" or "Q2False", wait=False)
        self.click(Q3==True and "Q3True" or "Q3False", wait=False)
        self.click(Q4==True and "Q4True" or "Q4False", wait=False) 
        self.click("QCalcResult")
        self.wait(self.speed['super slow'],self.speed['super slow']+0.05)
        self.download("graphCanvas")
        self.wait(self.speed['super slow'],self.speed['super slow']+0.05)
        graph = img2list()
        self.wait()
        print('graph\n',graph)
        result = {}
        try:
            result["Q1"] = Q1
            result["Q2"] = Q2
            result["Q3"] = Q3
            result["Q4"] = Q4
        except:
            pass
        try:
            result['minPrice'] = graph[2]
        except:
            result['minPrice'] = 'error'
        try:
            result['price'] = self.driver.find_element(By.XPATH,"//*[@id=\"app\"]/main/section/div/article/div[2]/div[1]/span/span").text.replace(',', '')
        except:
            result['price'] = 'error'
        try:
            result['maxPrice'] = graph[0]
        except:
            result['maxPrice'] = 'error'
        try:
            result['stdDate'] = self.driver.find_element(By.XPATH,self.elements["stdDate"]).text
        except:
            result['stdDate'] = 'error'
            pass
        return result
    #main process 
    def main(self):
        #접속
        self.access_url()
        
        print(len(self.diseases))
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        
        #각 질병 단위 루프
        for eachDisease in self.diseases:
            self.driver.quit()
            self.access_url()
            ActionChains(self.driver).move_by_offset(0, 0).perform()

            #각 테스트케이스 단위 테스트
            for eachCase in self.testcases :
                self.search_disease(eachDisease)
                RESULT = self.test(eachCase[0],eachCase[1],eachCase[2],eachCase[3])
                self.csv.write(eachDisease,eachCase[0],eachCase[1],eachCase[2],eachCase[3],RESULT["minPrice"],RESULT["price"], RESULT["maxPrice"], RESULT["stdDate"])
                self.wait(self.speed['super slow'],self.speed['super slow']+0.05)

crawler = Crawler()
crawler.main()