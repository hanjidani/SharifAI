import os
import random
import time

import cv2
import keras.models
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sklearn.utils import shuffle


def save_captcha(count, driver):
    driver.find_element(By.CSS_SELECTOR, "svg").screenshot("nums/" + str(count) + " - " + str(time.time()) + ".png")
    svg = driver.find_elements(By.CSS_SELECTOR, "path")
    l = [len(img.get_attribute('d')) for img in svg]
    driver.execute_script('document.getElementsByTagName("path").item(' + str(l.index(min(l))) + ').remove()')
    driver.find_element(By.CSS_SELECTOR, "svg").screenshot("nums/" + str(count) + " - " + str(time.time()) + ".png")
    svg = driver.find_elements(By.CSS_SELECTOR, "path")
    for img in svg:
        img.screenshot("nums/" + str(count) + " - " + str(time.time()) + ".png")


def retrive_captcha(st: int, en: int):
    op = Options()
    op.add_argument('--headless')
    i = st
    while i < en:
        rand = random.randint(0, 5)
        driver = webdriver.Chrome(options=op)
        driver.get("https://my.edu.sharif.edu")
        for j in range(rand):
            driver.find_element(By.CSS_SELECTOR, "a.ui.icon.button").click()
            time.sleep(1)
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/form/div/div[5]/div/a/i')))
            save_captcha(i, driver)
            time.sleep(3)
            print("iter no. ", str(i), " completed")
            i += 1
        driver.close()
        time.sleep(10)


def find_order(main_pic, seperated_pics):
    X = []
    for pic in seperated_pics:
        res = cv2.matchTemplate(main_pic, pic, cv2.TM_CCOEFF_NORMED)
        x = np.unravel_index(np.argmax(res), res.shape)
        X.append(x[1])
    # print(X)
    return [cv2.resize(x, (12, 16)) for _, x in sorted(zip(X, seperated_pics))]


def load_data(directory):
    imgs = []
    label = []
    for i in range(10):
        files = os.listdir(directory + str(i))
        for file in files:
            img = cv2.resize(cv2.imread(directory + str(i) + "/" + file, cv2.IMREAD_GRAYSCALE), (12, 16))
            imgs.append(img)
            label.append(i)
    return imgs, label


def AImodel(data, label):
    data, label = shuffle(data, label)
    tdata = data[:50]
    tlabel = label[:50]
    data = data[50:]
    # print(data)
    label = label[50:]

    # Build a model
    model = Sequential()
    model.add(Dense(512, activation='relu', input_shape=(12 * 16,)))
    model.add(Dense(10, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    data = np.array(data, dtype=np.float32)
    tdata = np.array(tdata, dtype=np.float32)
    # print(tdata.shape[0])
    tdata = tdata.reshape((tdata.shape[0], 12 * 16))
    data = data.reshape((data.shape[0], 12 * 16))
    label = to_categorical(label)
    tlabel = to_categorical(tlabel)
    # print(data.shape)
    model.fit(data, label, epochs=10, batch_size=225, validation_data=(tdata, tlabel))
    model.save("test.model2")
    return model


def get_page_captcha(driver):
    svg = driver.find_elements(By.CSS_SELECTOR, "path")
    l = [len(img.get_attribute('d')) for img in svg]
    driver.execute_script('document.getElementsByTagName("path").item(' + str(l.index(min(l))) + ').remove()')
    driver.find_element(By.CSS_SELECTOR, "svg").screenshot("main.png")
    svg = driver.find_elements(By.CSS_SELECTOR, "path")
    i = 0
    for img in svg:
        img.screenshot(str(i) + ".png")
        i += 1
    # load from disk
    main = cv2.imread("main.png", cv2.IMREAD_GRAYSCALE)
    imgs = []
    for i in range(4):
        imgs.append(cv2.imread(str(i) + ".png", cv2.IMREAD_GRAYSCALE))
    return find_order(main, imgs)


def predict(model_path, driver, lock):
    if not lock == None:
        lock.acquire()
    imgs = get_page_captcha(driver)
    model = keras.models.load_model(model_path)
    # print(imgs)
    imgs = np.array(imgs, dtype=np.float32) / 255.0
    imgs = imgs.reshape((imgs.shape[0], 12 * 16))
    pred = model.predict(imgs)
    if lock is not None:
        lock.release()
    return str(np.argmax(pred[0])) + str(np.argmax(pred[1])) + str(np.argmax(pred[2])) + str(np.argmax(pred[3]))


if __name__ == "__main__":
    pass

    # # fetch data from edu
    # retrive_captcha(50, 70)

    # # ordering a sample which located in ordering folder
    # showing_scale = 4
    # dir = "ordering/"
    # main_pic = cv2.imread(dir + "0.png")
    # seperated_pics = [cv2.imread(dir + str(i) + ".png") for i in range(1, 5)]
    # main_pic_show = cv2.resize(main_pic, (main_pic.shape[1] * showing_scale, main_pic.shape[0] * showing_scale))
    # cv2.imshow("main", main_pic_show)
    # i = 0
    # for img in find_order(main_pic, seperated_pics):
    #     i += 1
    #     img_show = cv2.resize(img, (img.shape[1] * showing_scale * 8, img.shape[0] * showing_scale * 8))
    #     cv2.imshow(str(i), img_show)
    # cv2.waitKey()

    # # label downloaded samples
    # dir_to_copy = "label/"
    # main_dir = "nums/"
    # # name_count = [4, 9, 6, 9, 10, 9, 12, 3, 9, 8]
    # name_count = [len(os.listdir(dir_to_copy + str(i))) for i in range(10)]
    # print(name_count)
    #
    # # print(len(name_count))
    # files = os.listdir("nums")
    # st: int = 31
    # remove_files = []
    # for file in files:
    #     index = file.find('-')
    #     # print(file, index)
    #     if int(file[:index].replace(" ", "")) < st:
    #         remove_files.append(file)
    # for i in remove_files:
    #     files.remove(i)
    # # print(files)
    # for file in files:
    #     img = cv2.imread(main_dir + file)
    #     img_show = cv2.resize(img,(img.shape[1] * 4, img.shape[0] * 4))
    #     cv2.imshow("main", img_show)
    #     key = cv2.waitKey()
    #     key -= 48
    #     if key < 0:
    #         continue
    #     print(file, key)
    #     shutil.copy(main_dir + file, dir_to_copy + str(key) + "/" + str(name_count[key]) + ".png")
    #     name_count[key] += 1

    # # Generate data
    # count = 50
    # dir_to_copy = "label/"
    # name_count = [len(os.listdir(dir_to_copy + str(i))) for i in range(10)]
    # name_count_var = name_count.copy()
    # for i in range(10):
    #     files = os.listdir(dir_to_copy + str(i))
    #     for j in range(name_count[i], count):
    #         print(i)
    #         shutil.copy(dir_to_copy + str(i) + "/" + random.choice(files),
    #                     dir_to_copy + str(i) + "/" + str(name_count_var[i]) + ".png")
    #         name_count_var[i] += 1

    # load data
    # directory = "label/"
    # imgs, label = load_data(directory)
    # model = AImodel(imgs, label)
    #

    # test the model
    # driver = webdriver.Chrome()
    # driver.get("https://my.edu.sharif.edu")
    # imgs = get_page_captcha(driver)
    # pred = predict("test.model", imgs)
    # driver.close()
    # print(np.argmax(pred[0]), np.argmax(pred[1]), np.argmax(pred[2]), np.argmax(pred[3]))
    # print(str(np.argmax(pred[0])), str(np.argmax(pred[1])), str(np.argmax(pred[2])), str(np.argmax(pred[3])))
