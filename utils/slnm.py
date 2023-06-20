from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def click_on_xpath(driver, wait_time, str_path):
  WebDriverWait(driver, wait_time).until(ec.element_to_be_clickable((By.XPATH, str_path))).click()
