import Crawler_tool
import Csv
import csv
import pandas as pd
from selenium.webdriver.common.by import By


crawler = Crawler_tool.Crawler()
target_url = "https://www.10000recipe.com/recipe/list.html?cat4=63&order=reco&page=2"
crawler.set_target_url(target_url)

page1_elems = {
  "recipe_type": "/html/body/dl/dd/div[1]/table/tbody/tr[1]/td/div/div[1]",
  "recipe_list": "/html/body/dl/dd/ul/ul",
}

def main():

  recipe_list_per_page = []

  crawler.wait(0.1, 0.3)
  item_xpath = page1_elems["recipe_list"] + "/li[contains(@class,'common_sp_list_li')]"
  list_url = crawler.target_url

  crawler.ensure_list_page(list_url)
  recipe_items = crawler.get_elems_xpath(item_xpath)
  i = 0
  for recipe_each in range(len(recipe_items)):
    recipe_items = crawler.get_elems_xpath(item_xpath)
    recipe = {}
    recipe_title_img = None
    recipe_title = ""
    recipe_ingredients = []
    recipe_steps = []
    
    print(f"[MK2] initial loop index={i}, item_count={len(recipe_items)}, url={crawler.current_url()}")
    
    
    #광고 닫기
    crawler._close_ad_overlays()


    #타깃 레시피 클릭해서 이동
    list_url = crawler.current_url()
    clicked = crawler.click(recipe_items[recipe_each])
    if not clicked:
      print(f"[MK2] skip index={i} due to click failure")
      continue

    crawler._close_ad_overlays()

    #레시피 내용 페이지에서 정보 수집
    #타이틀
    recipe_title = crawler.get_elem_class("view2_summary").find_element(By.TAG_NAME, "h3").text.strip()
    print("title : ", recipe_title)
    #재료
    ingredient_list = crawler.get_elem_id("divConfirmedMaterialArea").find_elements(By.XPATH, "./ul/li")
    for each in ingredient_list:
      ingredient_name = each.find_element(By.XPATH, "./div").text.strip()
      ingredient_quantity = each.find_element(By.XPATH, "./span").text.strip()
      print(f"ingredient: {ingredient_name}, quantity: {ingredient_quantity}")
      recipe_ingredients.append({
        "name": ingredient_name,
        "quantity": ingredient_quantity,
      })
    print("ingredients : ", recipe_ingredients, "\n")

    #광고 닫기
    crawler._close_ad_overlays()

    #조리 과정
    recipe_list = crawler.get_elem_id('obx_recipe_step_start').find_elements(By.XPATH, "./div")
    recipe_list = recipe_list[1:] #첫번째 div는 제목이므로 제외

    for each in recipe_list:
      try:
        step_description = each.find_element(By.XPATH, "./div[1]").text.strip()
        step_image = each.find_element(By.XPATH, "./div[2]/img").get_attribute("src")
        print("step description : ", step_description)
        print("step image : ", step_image)
        recipe_steps.append({
          "description": step_description,
          "image": step_image,
        })
      except Exception as e:
        break
    print("steps : ", recipe_steps, "\n\n")
    
    #광고 닫기
    crawler._close_ad_overlays()


    # 타이틀 이미지
    recipe_title_img = crawler.get_elem_id('main_thumbs').get_attribute("src")

    recipe = {
      "img": recipe_title_img,
      "title": recipe_title,
      "ingredients": recipe_ingredients,
      "steps": recipe_steps,
    }
    # print(f"[MK2] collected recipe data: {recipe}")

    recipe_list_per_page.append(recipe)

    #레시피 페이지로 돌아가기
    try:
      crawler.back(fallback_url=list_url)
    except Exception as e:
      print(f"[WARN] back failed: {e}")
    print(f"[MK2] after back url={crawler.current_url()}")
    crawler.dismiss_ads()
    crawler.wait(0.1, 0.3)
  print(recipe_list_per_page)
  pd.DataFrame(recipe_list_per_page).to_csv("recipes2.csv", index=True, encoding='utf-8-sig')
  
main()