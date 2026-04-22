from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import random


class Crawler:
  def __init__(self):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    self.driver = webdriver.Chrome(options=chrome_options)
    self.target_url = "https://www.10000recipe.com/recipe/list.html"
    self.driver.get(self.target_url)

    self.speed = {
      'super slow': 2.0,
      'slow': 1.0,
      'normal': 0.5,
      'fast': 0.1,
      'super fast': 0.05,
    }

  def wait(self, a=0.1, b=0.2):
    random_wait = random.uniform(a, b)
    time.sleep(random_wait)

  def get_elem_xpath(self, xpath):
    return self.driver.find_element(By.XPATH, xpath)

  def back(self, wait_a=0.0, wait_b=0.0, timeout=10):
    prev_url = self.driver.current_url
    self.driver.back()

    try:
      WebDriverWait(self.driver, timeout).until(lambda d: d.current_url != prev_url)
    except TimeoutException:
      self.driver.execute_script("window.history.go(-1);")
      WebDriverWait(self.driver, timeout).until(lambda d: d.current_url != prev_url)

    if wait_a != 0 and wait_b != 0:
      self.wait(wait_a, wait_b)

  def click(self, elem, wait_a=0, wait_b=0):
    # Reduce click interception by moving target into viewport center first.
    self.driver.execute_script(
      "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
      elem,
    )
    try:
      elem.click()
    except ElementClickInterceptedException:
      # Fallback to JS click when overlays/ads intercept native click.
      self.driver.execute_script("arguments[0].click();", elem)

    if wait_a != 0 and wait_b != 0:
      self.wait(wait_a, wait_b)

  def type(self, elem, text, wait_a=0, wait_b=0):
    elem.send_keys(text)
    if wait_a != 0 and wait_b != 0:
      self.wait(wait_a, wait_b)

  def download(self, elem, wait_a=0, wait_b=0):
    if wait_a != 0 and wait_b != 0:
      self.wait(wait_a, wait_b)
    return elem.screenshot("./resultGraph.png")
