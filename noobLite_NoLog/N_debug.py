import threading
from PIL import ImageGrab
from mouse import get_position as getPos
from humanize_zucc import *
from time import sleep
from quantumrand import cached_generator, randfloat, randint, get_data, hex, binary



print(grabPixel(897, 1022))


#C:\Program Files\Tesseract-OCR\tesseract.exe

#seed = cached_generator()
#print("done")
#for x in range(100):
#   print(randfloat(0, 100, seed))



def grabPixels(pixelX, pixelY):
    """ Grabs a pixel colour on a point of the screen."""
    try:
        return ImageGrab.grab().load()[pixelX, pixelY]
    except Exception as e:
        print('#ERROR Info {}\n'.format(e))  # pass


startTimerP = time()
promptStop = 10

on_off = 0


def finder():
    global on_off, x, y
    print("started")
    key = "q"
    while True:
        try:
            if is_pressed(key):
                # x, y = 0, 0
                if on_off == 0:
                    on_off = 1

                    print('mouse pos #1: {}'.format(getPos()))

                    [x, y] = getPos()
                    start = time()
                    colour = grabPixel(x, y)

                    print(time() - start)
                    print('colour #1: {}'.format(colour))
                elif on_off == 1:
                    on_off = 0
                    print('\nmouse pos #2: {}'.format(getPos()))

                    [xMax, yMax] = getPos()
                    start = time()
                    colour = grabPixels(xMax, yMax)

                    print(time() - start)
                    print('colour #2: {}\n'.format(colour))
                    print(f'Full Pos: {x}, {y}, {xMax}, {yMax}\n')
                while is_pressed(key):
                    sleep(0.01)
        except Exception as e:
            print("#ERROR debug Info {}\n".format(e))
        else:
            sleep(0.01)


finders = threading.Thread(target=finder)
finders.start()
