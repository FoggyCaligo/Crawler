from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
  ElementClickInterceptedException,
  TimeoutException,
  NoSuchElementException,
  StaleElementReferenceException,
)
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
      "super slow": 2.0,
      "slow": 1.0,
      "normal": 0.5,
      "fast": 0.1,
      "super fast": 0.05,
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
      self.driver.execute_script("window.history.back();")
      WebDriverWait(self.driver, timeout).until(lambda d: d.current_url != prev_url)

    if wait_a != 0 and wait_b != 0:
      self.wait(wait_a, wait_b)

  def is_ad(self):
    try:
      self.driver.find_element(By.ID, "ad_position_box")
      return True
    except NoSuchElementException:
      pass

    return bool(self.driver.execute_script("""
      const el = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2);
      if (!el) return false;
      if (el.tagName === 'IFRAME') return true;
      return !!el.closest('iframe');
    """))

  def _close_ad_overlays(self):
    close_selectors = [
      "[aria-label='닫기']",
      "[aria-label*='close']",
      ".close",
      ".btn_close",
      ".popup_close",
    ]
    for selector in close_selectors:
      for btn in self.driver.find_elements(By.CSS_SELECTOR, selector):
        try:
          if btn.is_displayed():
            self.driver.execute_script("arguments[0].click();", btn)
            self.wait(0.05, 0.15)
        except Exception:
          continue

    self.driver.execute_script("""
      const frames = Array.from(document.querySelectorAll('iframe'));
      const vw = window.innerWidth || document.documentElement.clientWidth;
      const vh = window.innerHeight || document.documentElement.clientHeight;
      for (const f of frames) {
        const src = (f.getAttribute('src') || '').toLowerCase();
        const id = (f.getAttribute('id') || '').toLowerCase();
        const r = f.getBoundingClientRect();
        const area = Math.max(0, r.width) * Math.max(0, r.height);
        const large = area > (vw * vh * 0.35);
        const fixedLike = getComputedStyle(f).position === 'fixed';
        const adLike = src.includes('googlesyndication') || id.startsWith('google_ads_iframe');
        if (adLike && (large || fixedLike)) {
          f.remove();
        }
      }
    """)

  def click(self, elem, wait_a=0, wait_b=0):
    max_attempts = 4
    last_error = None

    for _ in range(max_attempts):
      try:
        self.driver.execute_script(
          "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
          elem,
        )
        elem.click()
        last_error = None
        break
      except (ElementClickInterceptedException, StaleElementReferenceException) as e:
        last_error = e
        self._close_ad_overlays()
        try:
          self.driver.execute_script("arguments[0].click();", elem)
          last_error = None
          break
        except Exception as js_error:
          last_error = js_error
          self.wait(0.08, 0.2)

    if last_error is not None:
      raise last_error

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
