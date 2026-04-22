
import Crawler
from selenium.webdriver.common.by import By
crawler = Crawler.Crawler()



page1_elems = {
  "recipe_type": "/html/body/dl/dd/div[1]/table/tbody/tr[1]/td/div/div[1]",
  "recipe_list": "/html/body/dl/dd/ul/ul"
}



def main():
  recipe_type_elem = crawler.get_elem_xpath(page1_elems["recipe_type"])
  recipe_list_elem = crawler.get_elem_xpath(page1_elems["recipe_list"])

  recipe_items = recipe_list_elem.find_elements(By.XPATH, "./li")

  for i in range(len(recipe_items)):
    crawler.wait()
    crawler.click(crawler.get_elem_xpath(page1_elems["recipe_list"]+f"/li[{i+1}]"))
    crawler.back(wait_a=0.1, wait_b=0.3)
    crawler.back(wait_a=0.1, wait_b=0.3)
    print("back")


main()
