import time
from bibliopixel import *
from bibliopixel.animation import sequence
from bibliopixel.drivers.PiWS281X import PiWS281X
from BiblioPixelAnimations.matrix.bloom import Bloom
from BiblioPixelAnimations.matrix.GameOfLife import GameOfLife
from BiblioPixelAnimations.matrix.MatrixRain import MatrixRain
from bibliopixel.animation.sequence import Sequence

driver = PiWS281X(300)
layout = LEDMatrix(driver, width=50, height=6,
                   serpentine=True, threadedUpdate=False)

sequence = Sequence(layout)

# #Load animations into Queue
bloom = Bloom(layout)
# #run at 15fps, for 10 seconds
sequence.add_animation(bloom, amt=6, fps=15, max_steps=150)

gol = GameOfLife(layout)
# #run at queue default framerate, until simulation completes twice
sequence.add_animation(gol, max_cycles=2)

rain = MatrixRain(layout)
#run at queue default framerate for 300 steps
sequence.add_animation(rain, amt=4, max_steps=300)


try:
    #run animations at default 30fps
    sequence.run()

except KeyboardInterrupt:
    # Ctrl+C will exit the animation and turn the LEDs offs
    layout.all_off()
    layout.update()
    print("Done!")
