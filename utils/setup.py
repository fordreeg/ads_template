import sys
import time
import traceback

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from termcolor import cprint


def line_control(file_txt):
  with open(file_txt) as f1:
    lines = f1.readlines()
    non_empty_lines = (line for line in lines if not line.isspace())
    with open(file_txt, "w") as n_f1:
      n_f1.writelines(non_empty_lines)


def prepare_profile_launch(index, profile_id, main_callback):
  profile_number = index + 1
  args = str(["--disable-popup-blocking", "--window-position=700,0"]).replace("'", '"')
  open_profile_url = f"http://local.adspower.net:50325/api/v1/browser/start?user_id={profile_id}&launch_args={str(args)}"
  close_profile_url = f"http://local.adspower.net:50325/api/v1/browser/stop?user_id={profile_id}"

  try:
    resp = requests.get(open_profile_url).json()
    time.sleep(.5)

    while True:
      try:
        chrome_driver = resp["data"]["webdriver"]
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(service=Service(chrome_driver), options=chrome_options)
        break
      except KeyError:
        requests.get(open_profile_url).json()
        time.sleep(3)
        requests.get(close_profile_url).json()
      except Exception as ex:
        cprint(str(ex), 'red')
        cprint('----------------------', 'red')
        cprint(f'{profile_id} - profile opening error', 'red')
        driver.quit()
        requests.get(close_profile_url)
        break

    main_callback(driver, close_profile_url)

    cprint(f'{profile_number}. {profile_id} - done', 'green')

  except requests.exceptions.ConnectionError:
    cprint(f'Adspower is not running.', 'red')
    sys.exit(0)
  except requests.exceptions.JSONDecodeError:
    cprint(f'Check yor connection. You should turn off VPN/Proxy.', 'red')
    sys.exit(0)

  except TimeoutException:
    time.sleep(.3)
    cprint(f'Profile < {profile_id} >  has TimeOut Error.', 'red')
    driver.quit()
    requests.get(close_profile_url)

  except WebDriverException as err:
    if 'LavaMoat' in str(err):
      cprint(f'Profile < {profile_id} >  has LavaMoat Error', 'red')
    else:
      traceback.print_exc()
      time.sleep(.3)
      cprint(f'WebDriverException Error', 'red')
    driver.quit()
    requests.get(close_profile_url)

  except Exception:
    traceback.print_exc()
    time.sleep(.3)
    cprint(f'{profile_number}. {profile_id} = already done', 'yellow')
    driver.quit()
    requests.get(close_profile_url)


def initialize_main(main):
  line_control("id_users.txt")
  with open("id_users.txt", "r") as f:
    id_users = [row.strip() for row in f]

  for idx, ads_id in enumerate(id_users):
    try:
      prepare_profile_launch(idx, ads_id, main)
    except IndexError:
      cprint(f'Some problem in the id_users.txt', 'red')
      sys.exit(0)
    except Exception as ex:
      cprint(str(ex), 'red')
