import threading
from lib2to3.pgen2 import driver
from typing import final
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as dt
import time

import captcha

def change(studentID, passWD, moment, lock):
    driver = webdriver.Chrome()
    driver.get("https://my.edu.sharif.edu")
    # driver.fullscreen_window()
    driver.set_window_size(1920, 1080)
    # print(driver.current_url)
    while driver.current_url == "https://my.edu.sharif.edu/":
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "username").send_keys(str(studentID))
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "password").send_keys(str(passWD))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'path')))
        driver.find_element(By.NAME, "securityCode").send_keys(captcha.predict("test.model", driver, lock))
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/form/div/button').click()
        try:
            WebDriverWait(driver, 5).until_not(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/form/div/button')))
        except:
            continue
    WebDriverWait(driver, 600).until(EC.url_to_be("https://my.edu.sharif.edu/courses/offered"))
    WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.CLASS_NAME, "field")))
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/a[2]').click()
    WebDriverWait(driver, 600).until(EC.url_to_be("https://my.edu.sharif.edu/courses/marked"))
    courses = driver.find_elements(By.CSS_SELECTOR,
                                   "button.ui.mini.basic.circular.icon.button:not(button.ui.yellow.mini.basic.circular"
                                   ".icon.button), button.ui.blue.mini.basic.circular.icon.button:not(button.ui.yellow"
                                   ".mini.basic.circular.icon.button")
    now = dt.now()
    time.sleep(max(0, int((moment - now).total_seconds())))
    time.sleep(0.5)

    el = driver.find_element(By.CSS_SELECTOR, "button.button.ui.icon.primary.right.labeled.button")
    try:
        el.click()
        print("done!")
    except:
        print("undone! :(")
    driver.close()