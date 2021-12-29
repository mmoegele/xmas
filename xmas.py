import os
import time
import board
import neopixel
import datetime
import logging
from flask import Flask, render_template
from threading import Thread

global animationThread
global should_run
should_run = True

LED_COLUMN = 6
LED_ROW = 50      # Number of LED pixels.
LED_PIN = board.D18      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 0.2     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.


# The number of NeoPixels


# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB
logFile = os.path.dirname(os.path.abspath(__file__)) + "/log.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(logFile),
        logging.StreamHandler()
    ]
)

pixels = neopixel.NeoPixel(
    LED_PIN, LED_ROW * LED_COLUMN, brightness=LED_BRIGHTNESS, auto_write=False, pixel_order=ORDER
)


# Define functions which animate LEDs in various ways.


def map_matrix(x, y):
    if x < 1:
        indexValue = y
    elif (x + 1) % 2 == 0:
        indexValue = (x+1)*LED_ROW - y - 1
    else:
        indexValue = x*LED_ROW + y
    # print(str(x) + ";" + str(y) + ";" + str(indexValue))
    return indexValue


def set_row_color(pixels, row_index, color=(255, 0, 0),  wait_ms=20):
    for x in range(LED_COLUMN):
        pixels[map_matrix(x, row_index)] = color


def set_col_color(pixels, col_index, color=(255, 0, 0),  wait_ms=20):
    for x in range(LED_ROW):
        pixels[map_matrix(col_index, x)] = color


def xmas_tree_raise_up(pixels, color=(255, 255, 255), bkcolor=(50, 0, 0), wait_ms=20, iterations=5):
    for i in range(iterations):
        pixels.fill(bkcolor)
        # time.sleep(wait_ms/1000)

        for y in range(LED_ROW):
            set_row_color(pixels, y, color)
            # map_matrix(x, y)
            pixels.show()
            time.sleep(wait_ms/1000)


def xmas_tree_raise_down(pixels, color=(255, 255, 255), bkcolor=(50, 0, 0), wait_ms=20, iterations=5):
    for i in range(iterations):
        pixels.fill(bkcolor)
        # time.sleep(wait_ms/1000.0)

        for y in range(LED_ROW, 0, -1):
            set_row_color(pixels, y, color)
            pixels.show()
            time.sleep(wait_ms/1000)


def xmas_tree_raise_left(pixels, color=(255, 255, 255), bkcolor=(20, 20, 20), wait_ms=20, iterations=5):
    for i in range(iterations):
        pixels.fill(bkcolor)
        # time.sleep(wait_ms/1000.0)

        for y in range(LED_COLUMN):
            set_col_color(pixels, y, color)
            pixels.show()
            time.sleep(wait_ms/1000)


def colorWipe(pixels, color, wait_ms=20):
    """Wipe color across display a pixel at a time."""
    for y in range(LED_ROW):
        set_row_color(pixels, y, color)
        pixels.show()
        time.sleep(wait_ms/1000.0)


def uni_color(pixels, color=(255, 255, 255), wait_ms=50, iterations=5):
    global should_run
    for i in range(iterations):
        pixels.fill(color)
        pixels.show()

        if should_run == False:
            break
        time.sleep(wait_ms/1000.0)


def snake_color(pixels, color=(255, 255, 255), bkcolor=(50, 0, 0), wait_ms=20, iterations=5):
    global should_run
    for i in range(iterations):
        pixels.fill(bkcolor)

        for x in range(LED_COLUMN*LED_ROW):
            pixels[x] = color
            pixels.show()

            if should_run == False:
                break
            time.sleep(wait_ms/1000.0)


def xmas_tree_pattern(pixels, color=(255, 255, 255), bkcolor=(50, 0, 0), rowHeight=6, wait_ms=50, iterations=5):
    global should_run

    for i in range(iterations):
        pixels.fill(bkcolor)
        time.sleep(wait_ms/1000.0)

        for y in range(LED_ROW):
            set_row_color(pixels, y, color)
            # map_matrix(x, y)
            if y > rowHeight:
                set_row_color(pixels, y - rowHeight, bkcolor)
            pixels.show()

            if should_run == False:
                break
            time.sleep(wait_ms/1000.0)

        for i in range(LED_ROW - rowHeight, LED_ROW):
            set_row_color(pixels, i, bkcolor)
            pixels.show()
            if should_run == False:
                break
            time.sleep(wait_ms/1000.0)


def xmas_tree_spiral(pixels, color=(255, 255, 255), bkcolor=(50, 0, 0), wait_ms=50, iterations=5):
    patternHeight = 7
    global should_run

    for j in range(iterations):
        for i in range(patternHeight):
            pixels.fill(bkcolor)
            for y in range(0, LED_ROW, patternHeight):
                for x in range(LED_COLUMN):
                    if patternHeight == 2:
                        pixels[map_matrix(x, x + y + i - 2)] = color
                    if patternHeight == 1:
                        pixels[map_matrix(x, x + y + i - 1)] = color

                    pixels[map_matrix(x, x + y + i)] = color
                    pixels[map_matrix(x, x + y + 1 + i)] = color
                    pixels[map_matrix(x, x + y + 2 + i)] = color

            pixels.show()
            if should_run == False:
                break
            time.sleep(wait_ms/1000.0)


# def theaterChase(pixels, color, wait_ms=50, iterations=10):
#    """Movie theater light style chaser animation."""
#    for j in range(iterations):
#        for q in range(3):
#            for i in range(0, LED_ROW * LED_COLUMN, 3):
#                pixels[i] = color
#            pixels.show()
#            time.sleep(wait_ms/1000.0)
#            for i in range(0, LED_ROW * LED_COLUMN, 3):
#                pixels[i] =  0


def rainbow(pixels, wait_ms=20, iterations=1):
    global should_run
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(LED_ROW * LED_COLUMN):
            pixels[i] = wheel((i+j) & 255)
        pixels.show()
        if should_run == False:
            break
        time.sleep(wait_ms/1000.0)


def rainbowCycle(pixels, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    global should_run
    for j in range(256*iterations):
        for i in range(LED_ROW * LED_COLUMN):
            pixels[i] = wheel((int(i * 256 / LED_ROW) + j) & 255)
        pixels.show()

        if should_run == False:
            break
        time.sleep(wait_ms/1000.0)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    #print("r:" + str(r) + " g:" + str(g) + " b: " + str(b))

    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


# def rainbow_cycle(wait):
#     for j in range(255):
#         for i in range(LED_ROW):
#             pixel_index = (i * 256 // LED_ROW) + j
#             pixels[i] = wheel(pixel_index & 255)
#         pixels.show()
#         time.sleep(wait)

def checkRun():
    now = datetime.datetime.now()
    logging.info(now)

    if (now.hour >= 5 and now.hour < 10):
        logging.info("checkRun morning")
        return True
    elif (now.hour >= 16 and now.hour <= 23):
        logging.info("checkRun evening")
        return True
    else:
        logging.info("checkRun off time")
        return False


animations = {
    1: {'name': 'Uni Color', 'color': (255, 255, 255), 'bkcolor': (0, 0, 0)},
    2: {'name': 'Snake Color', 'color': (255, 255, 255), 'bkcolor': (0, 0, 0)},
    4: {'name': 'tree raise left', 'color': (255, 255, 255), 'bkcolor': (0, 0, 0)},
    8: {'name': 'tree raise up', 'color': (255, 255, 255), 'bkcolor': (0, 0, 0)},
}


def getCPUTemp():
    try:
        tFile = open('/sys/class/thermal/thermal_zone0/temp')
        temp = float(tFile.read())
        tempC = temp/1000
        return tempC

    except:
        return -100


def runAnimation(animationNumber=2047):
    global should_run
    should_run = True
    logging.info(animationNumber)

    while should_run:
        # theaterChase(pixels,(255, 0, 0) )
        # rainbowCycle(pixels)
        # rainbow(pixels)
        shortwaitTime = 100
        longwaitTime = 5000
        iteration = 10

        for i in range(0, 255, 10):
            if checkRun():
                if should_run == False:
                    break

                color = wheel(i)
                bkcolor = wheel(255 - i)

                if (animationNumber & 1 == 1):
                    uni_color(pixels=pixels, wait_ms=longwaitTime,
                              color=(255, 255, 255), iterations=1)

                if (animationNumber & 2 == 2):
                    uni_color(pixels=pixels, wait_ms=longwaitTime, color=color)

                if (animationNumber & 4 == 4):
                     xmas_tree_raise_left(pixels, color, bkcolor,
                                 longwaitTime, iteration)

                if (animationNumber & 8 == 8):
                    snake_color(pixels=pixels, color=color,
                                bkcolor=bkcolor, wait_ms=shortwaitTime, iterations=iteration)

                if (animationNumber & 16 == 16):
                    for i in range(10):
                        if should_run == False:
                            break
                        xmas_tree_raise_up(
                            pixels, color, bkcolor, shortwaitTime, iteration)
                        xmas_tree_raise_down(
                            pixels, bkcolor, color, shortwaitTime, iteration)

                if (animationNumber & 32 == 32):
                    xmas_tree_pattern(pixels=pixels, color=color,
                                      bkcolor=bkcolor, wait_ms=shortwaitTime, iterations=1)

                if (animationNumber & 64 == 64):
                    xmas_tree_spiral(pixels=pixels, color=color,
                                     bkcolor=bkcolor, wait_ms=shortwaitTime, iterations=1)

                if (animationNumber & 128 == 128):
                    snake_color(pixels=pixels, color=color,
                                bkcolor=bkcolor, wait_ms=shortwaitTime, iterations=1)

        else:
            colorWipe(pixels, (0, 0, 0), 10)
            animationNumber = 2047
            time.sleep(5)
        # xmas_tree_spiral(pixels)


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", CPUTemperatur=str(getCPUTemp()))


@app.route("/<animationId>/<color>/<bkcolor>")
def action(animationId, color, bkcolor):
    httpErrorCode = 200
    # Convert the pin from the URL into an integer:
    try:
        intAnimationId = int(animationId)
        global should_run
        global animationThread
        should_run = False
        animationThread.join()
        animationThread = Thread(
            target=runAnimation, args=(intAnimationId,), daemon=True)
        animationThread.start()
    except ValueError as e:
        logging.error(e)
        httpErrorCode = 500

    return render_template("changeAnimation.html", AnimationId=str(intAnimationId), CPUTemperatur=str(getCPUTemp()))


# Main program logic follows:
if __name__ == '__main__':
    try:
        # runAnimation()
        should_run = True
        animationThread = Thread(target=runAnimation, daemon=True)
        animationThread.start()
        app.run(debug=False, port=80, host='0.0.0.0')
        should_run = False
        print('wait until animation is stopped')
        animationThread.join()

        colorWipe(pixels, (0, 0, 0), 10)
    except KeyboardInterrupt:
        print('exit.')
        colorWipe(pixels, (0, 0, 0), 10)
