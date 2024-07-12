import time
from datetime import datetime as dt

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import captcha


def choose_for_me(studentID, passWD, moment, index, lock):
    print("choosing for:", studentID, passWD, index)
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
    # print(courses)
    # moment = dt(2022, 9, 7, 8, 0, 0, 0)
    # moment = dt(2022, 9, 6, 22, 31, 0, 0)
    course = courses[index]
    if course.get_attribute('class') == 'ui mini basic circular icon button':
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(course))
        # element = WebDriverWait(driver, 20).until_not(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "button.cui.small.floating.icon.message")))

        course.click()

        # element = WebDriverWait(driver, 20).until_not(
        # EC.presence_of_element_located((By.CSS_SELECTOR, "button.ui.small.floating.icon.message")))
        el = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/button[2]")
        # print(el)
        # element = WebDriverWait(driver, 20).until_not(
        # EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui.small.floating.icon.message")))
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(el))
        now = dt.now()
        time.sleep(max(0, int((moment - now).total_seconds())))
        # time.sleep(0.050)
        try:
            el.click()
            WebDriverWait(driver, 60).until(EC.invisibility_of_element(el))
        except:
            return

    print(index)
    driver.close()
