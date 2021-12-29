import datetime
import logging
import os
from time import sleep
import time
from threading import Thread
from flask import Flask, render_template

def checkRun(animationId=0):
    global should_run
    should_run = True

    while should_run:
        now = datetime.datetime.now()
        for i in range(50):
            if should_run == False:
                break

            time.sleep(5)
            print(now)
            print(animationId)
            if (now.hour > 5 and now.hour < 8):
                print("checkRun morning")

            elif (now.hour > 16 and now.hour < 23):
                print("checkRun evening")

            else:
                print("checkRun off time")


app = Flask(__name__)
global animationThread
animationThread = Thread(target=checkRun)


@app.route('/')
def home():
    return render_template("index.html", CPUTemperatur="222")


@app.route("/<animationId>/<color>")
def action(animationId, action):
    # Convert the pin from the URL into an integer:
    animationId = int(animationId)
    global should_run
    global animationThread
    should_run = False
    animationThread.join()

    animationThread = Thread(target=checkRun, args=(animationId,))
    animationThread.start()

    return 'Hello world ' + str(animationId)


def getCPUTemp():
    try:
        tFile = open('/sys/class/thermal/thermal_zone0/temp')
        temp = float(tFile.read())
        tempC = temp/1000
        return tempC

    except:
        return -100


if __name__ == '__main__':
    try:
        print(getCPUTemp())
        now = datetime.datetime.now()
        time.sleep(5)
        # Start Thread

        animationThread.start()

       # app.thread.start()
        app.run(debug=False, port=80, host='0.0.0.0')
        print('Press Ctrl-C to quit.')
        # rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

    except KeyboardInterrupt:
        print('Exit')
