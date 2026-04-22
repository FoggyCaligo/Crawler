
import Crawler
from selenium.webdriver.common.by import By
crawler = Crawler.Crawler()



page1_elems = {
  "recipe_type": "/html/body/dl/dd/div[1]/table/tbody/tr[1]/td/div/div[1]",
  "recipe_list": "/html/body/dl/dd/ul/ul"
}



def main():
  crawler.wait(0.1, 0.3)
  recipe_list_elem = crawler.get_elem_xpath(page1_elems["recipe_list"])
  recipe_items = recipe_list_elem.find_elements(By.XPATH, "./li")
  for i in range(len(recipe_items)-1):
    #레시피 클릭
    crawler.wait(0.1, 0.3)
    if(crawler.is_ad()):
      crawler.back()
    crawler.click(crawler.get_elem_xpath(page1_elems["recipe_list"]+f"/li[{i+1}]"))
    #뒤로가기
    crawler.back()
    if(crawler.is_ad()):
      crawler.back()


    crawler.wait(0.1, 0.3)


main()
