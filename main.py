import time
import requests
from utils.setup import initialize_main

target_url = 'https://google.com'


def main(driver, close_profile_url):
  time.sleep(2)
  driver.switch_to.new_window()
  time.sleep(.5)
  driver.get(target_url)
  time.sleep(1)
  driver.quit()
  requests.get(close_profile_url)


if __name__ == '__main__':
  initialize_main(main)
