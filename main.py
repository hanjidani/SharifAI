import time

import groupchange
import run
from datetime import datetime as dt
import tensorflow as tf
import threading

import run2

if __name__ == '__main__':
    # moment = dt(2022, 9, 7, 8, 0, 0, 0)
    # studentIDs = ["99102189"]
    # passWDs = ["138113811381Tt"]
    studentIDs = ["400100746"]
    passWDs = ["Ho13811381"]
    # change = [2,0]
    # moment = dt(2023, 2, 14, 7, 49, 2, 0)
    # momentt = dt(2023, 2, 14, 7, 46, 4, 0)
    moment = dt(2023, 9, 11, 8, 0, 0, 0)
    # momentt = dt(2023, 2, 14, 8, 0, 4, 0)
    # studentIDs = ["400109254", "400109254"]
    # passWDs = ["0150341660", "0150341660"]
    # lessons = [5,1]
    # run.choose_for_me(studentIDs[0], passWDs[0], moment, 0)
    # lock = threading.Lock()
    # start_time = time.time()
    # for i in range(len(studentIDs)):
        # for j in range(lessons[i]):
        #     t = threading.Thread(target=run.choose_for_me, args=[studentIDs[i], passWDs[i], moment, j, lock])
        #     t.start()
        #     time.sleep(0.5)
        # t = threading.Thread(target=run2.choose_for_me, args=[studentIDs[i], passWDs[i], moment])
        # t.start()
        # for j in range(change[i]):
        #     t = threading.Thread(target=groupchange.change, args=[studentIDs[i], passWDs[i], moment, lock])
        #     t.start()
        #     time.sleep(0.5)
    # for i in range(len(studentIDs)):
    #     # t = threading.Thread(target=run2.choose_for_me, args=[studentIDs[i], passWDs[i], moment])
    #     # t.start()
    #     flag = False
    #     while not flag:
    #         flag = run2.choose_for_me(studentID=studentIDs[i], passWD=passWDs[i], moment=moment)
    #     # time.sleep(1)
    #     # t = threading.Thread(target=run2.choose_for_me, args=[studentIDs[i], passWDs[i], momentt])
    #     # t.start()
    run2.choose_for_me()
