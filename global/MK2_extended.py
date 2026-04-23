import Crawler_tool
import pandas as pd
from selenium.webdriver.common.by import By

crawler = Crawler_tool.Crawler()

page1_elems = {
    "recipe_type": "/html/body/dl/dd/div[1]/table/tbody/tr[1]/td/div/div[1]",
    "recipe_list": "/html/body/dl/dd/ul/ul",
}

page2_elems = {
    "recipe_title": "/html/body/div[6]/div[1]/div[3]/h3",
    "recipe_quantity": "/html/body/div[6]/div[1]/div[3]/div[2]/span[1]",
    "recipe_time": "/html/body/div[6]/div[1]/div[3]/div[2]/span[2]",
    "recipe_difficulty": "/html/body/div[6]/div[1]/div[3]/div[2]/span[3]",
    "ingredient_list": "/html/body/div[6]/div[1]/div[6]/div[2]/ul",
    "recipe": "/html/body/div[6]/div[1]/div[14]",
}


def _safe_text_from_element(element, by, locator, default=""):
    try:
        return element.find_element(by, locator).text.strip()
    except Exception:
        return default


def _safe_attr_from_element(element, by, locator, attr_name, default=""):
    try:
        value = element.find_element(by, locator).get_attribute(attr_name)
        return value.strip() if isinstance(value, str) else (value or default)
    except Exception:
        return default


def main():
    recipe_list_per_page = []

    crawler.wait(0.1, 0.3)
    item_xpath = page1_elems["recipe_list"] + "/li[contains(@class,'common_sp_list_li')]"
    list_url = crawler.target_url

    crawler.ensure_list_page(list_url)
    recipe_items = crawler.get_elems_xpath(item_xpath)

    for index in range(len(recipe_items)):
        crawler.ensure_list_page(list_url)
        recipe_items = crawler.get_elems_xpath(item_xpath)

        if index >= len(recipe_items):
            print(f"[MK2] skip index={index} because current item_count={len(recipe_items)}")
            continue

        recipe_title_img = ""
        recipe_title = ""
        recipe_quantity = ""
        recipe_time = ""
        recipe_difficulty = ""
        recipe_ingredients = []
        recipe_steps = []

        print(f"[MK2] loop index={index}, item_count={len(recipe_items)}, url={crawler.current_url()}")

        crawler._close_ad_overlays()

        list_url = crawler.current_url()
        clicked = crawler.click(recipe_items[index])
        if not clicked:
            print(f"[MK2] skip index={index} due to click failure")
            continue

        crawler._close_ad_overlays()

        try:
            summary = crawler.get_elem_class("view2_summary")

            recipe_title = _safe_text_from_element(summary, By.TAG_NAME, "h3")
            recipe_quantity = _safe_text_from_element(
                summary,
                By.XPATH,
                ".//div[contains(@class, 'view2_summary_info')]//span[1]",
            )
            recipe_time = _safe_text_from_element(
                summary,
                By.XPATH,
                ".//div[contains(@class, 'view2_summary_info')]//span[2]",
            )
            recipe_difficulty = _safe_text_from_element(
                summary,
                By.XPATH,
                ".//div[contains(@class, 'view2_summary_info')]//span[3]",
            )

            recipe_title_img = crawler.get_elem_id('main_thumbs').get_attribute("src") or ""

            print("title :", recipe_title)
            print("quantity :", recipe_quantity)
            print("time :", recipe_time)
            print("difficulty :", recipe_difficulty)
            print("image :", recipe_title_img)

            ingredient_list = crawler.get_elems_xpath(page2_elems["ingredient_list"] + "/li")
            for ingredient_item in ingredient_list:
                ingredient_name = _safe_text_from_element(ingredient_item, By.XPATH, "./div")
                ingredient_quantity = _safe_text_from_element(ingredient_item, By.XPATH, "./span")
                print(f"ingredient: {ingredient_name}, quantity: {ingredient_quantity}")
                recipe_ingredients.append({
                    "name": ingredient_name,
                    "quantity": ingredient_quantity,
                })
            print("ingredients :", recipe_ingredients)

            crawler._close_ad_overlays()

            step_blocks = crawler.get_elem_id('obx_recipe_step_start').find_elements(By.XPATH, "./div")
            step_blocks = step_blocks[1:]

            for step_block in step_blocks:
                step_description = _safe_text_from_element(step_block, By.XPATH, "./div[1]")
                step_image = _safe_attr_from_element(step_block, By.XPATH, "./div[2]/img", "src")

                if not step_description and not step_image:
                    continue

                print("step description :", step_description)
                print("step image :", step_image)
                recipe_steps.append({
                    "description": step_description,
                    "image": step_image,
                })
            print("steps :", recipe_steps)

            recipe = {
                "img": recipe_title_img,
                "title": recipe_title,
                "quantity": recipe_quantity,
                "time": recipe_time,
                "difficulty": recipe_difficulty,
                "ingredients": recipe_ingredients,
                "steps": recipe_steps,
            }
            print(f"[MK2] collected recipe data: {recipe}")

            recipe_list_per_page.append(recipe)
            print(f"[MK2] appended recipe, total_count={len(recipe_list_per_page)}")

        except Exception as e:
            print(f"[ERROR] recipe parse failed at index={index}: {e}")

        finally:
            crawler._close_ad_overlays()
            try:
                crawler.back(fallback_url=list_url)
            except Exception as e:
                print(f"[WARN] back failed: {e}")
            print(f"[MK2] after back url={crawler.current_url()}")
            crawler.dismiss_ads()
            crawler.wait(0.1, 0.3)

    print(recipe_list_per_page)
    Csv.save_to_csv(recipe_list_per_page, "recipes.csv")

    try:
        crawler.driver.quit()
    except Exception:
        pass


if __name__ == "__main__":
    main()
