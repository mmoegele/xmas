from bibliopixel import LEDStrip
#import the module you'd like to use
from BiblioPixelAnimations.strip import Rainbows
from bibliopixel.drivers.PiWS281X import PiWS281X
#init driver with the type and count of LEDs you're using
driver     = PiWS281X(300)

#init controller
led = LEDStrip(driver)

#init animation; replace with whichever animation you'd like to use
anim = Rainbows.RainbowCycle(led)

try:
    #run the animation
    anim.run()
except KeyboardInterrupt:
    #Ctrl+C will exit the animation and turn the LEDs offs
    led.all_off()
    led.update()