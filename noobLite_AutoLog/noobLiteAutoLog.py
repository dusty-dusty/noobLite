# https://i.imgur.com/N0hjFXb.png fix inspection if needed
# http://cookie.riimu.net/speed/
# https://stackoverflow.com/questions/15208615/using-pth-files
import threading
from time import sleep, strftime, time

# Only change BELOW these values. Unless you know what you are doing

key = "'"  # toggle key. change to whatever you want
fkey = 'f10' # fkey for logout

minimapX, minimapY, minimapXMax, minimapYMax = 1437, 37, 1626, 235  # use n_debug to get these values. Only need to do once

logColour = (72, 39, 42)  # use n_debug to get these values. Only need to do once
logColourLocationX, logColourLocationY = 1412, 510  # use n_debug to get these values. Only need to do once
logButtonX, logButtonY, logButtonXMax, logButtonYMax = 1371, 514, 1589, 738

humanReactionTime = False  # Change to True if you want the mouse to move slower and human like. I would not enable tbh

# Only change ABOVE these values. Unless you know what you are doing

# for debugging not really needed in this script
count1 = 0
count2 = 0
count3 = 0
count4 = 0
countTime = 0
superCountTime = 0
fastClick = 0
waitClick = 0
# for debugging not really needed in this script

forceStop = False
hours = 24
timerLimit = (hours * 60) * 60
totalTime = 0
tTime = 0

on_off = 0
startTime = time()
sleepTimer = time()
# print(f"Afk will be {hours} hours, take a small break after it ends.")
# print("Check the pictures in this folder to show you how to set up.")
# print("Make sure to wear dark cape")
# print("then press ' to start the script")
# print(f'afk timer is {timerLimit / 60} min')

# amount = 0

## all under is for my brain file that I dont want to release so im copy pasting part of it here
import mss
from logging import getLogger, INFO
from time import sleep, strftime, time
from quantumrand import cached_generator, randfloat, randint, get_data, hex, binary
from keyboard import wait, send, add_hotkey, on_press, is_pressed, press as kpress, release as krelease, write
from mouse import get_position, move, press, release, wheel

from PIL import ImageGrab

seed = cached_generator()


def enableLogger(name):
    print("called")
    # key = ''  # wont work unless you get your own key.
    logs = getLogger('logdna')
    # logs.setLevel(INFO)
    # options = {'hostname': name, 'index_meta': True, 'include_standard_meta': False}
    # logInput = LogDNAHandler(key, options)
    # logs.addHandler(logInput)
    return logs


log = enableLogger('Bot')


def pixelMatchesColor(colour, match, tolerance=0):
    """Matches a pixel colour on a point of the screen."""
    # should always be 3 or 4 (rbg, possibly with an alpha channel)
    if colour == match:  # exact match
        # print("exact match")
        return True
    hasMatched = True
    if tolerance > 0:
        for index in range(len(colour)):  # make sure all 3 match
            if colour[index] - tolerance > match[index]:  # too high
                hasMatched = False
            elif colour[index] + tolerance < match[index]:  # too low
                hasMatched = False
    if hasMatched:
        # print("found ")
        return True
    else:
        # print(f"{colour} not found ")
        return False


def pixelFindColour(colour, numberX, numberY, numberXMax, numberYMax, tolerance=0, boolValue=False):
    """Finds and Matches a pixel colour on screen."""
    box = {"left": numberX, "top": numberY, "width": numberXMax - numberX, "height": numberYMax - numberY, }
    try:
        with mss.mss() as sct:
            img = sct.grab(box)
            pixels = zip(img.raw[2::4], img.raw[1::4], img.raw[0::4])

            for checked, matchFind in enumerate(pixels):
                # print(matchFind)
                if matchFind == colour:  # exact match
                    areaHeight = int(checked / box["width"])
                    totalArea = checked - (areaHeight * box["width"])  # removes checked pixles from total pixels
                    x = numberX + totalArea  # lengthArea
                    y = numberY + areaHeight  # heightArea
                    if boolValue:
                        print(f"found match = {(x, y)} {colour}")
                        return True
                    else:
                        # print(f"found match = {(x, y)} {colour}")
                        return x, y
                elif tolerance > 0:
                    hasMatched = True
                    for index in range(len(colour)):  # make sure all r,g,b match all 3
                        if colour[index] - tolerance > matchFind[index]:  # too high
                            hasMatched = False
                        elif colour[index] + tolerance < matchFind[index]:  # too low
                            hasMatched = False
                    if hasMatched:
                        areaHeight = int(checked / box["width"])
                        totalArea = checked - (areaHeight * box["width"])  # removes checked pixles from total pixels
                        x = numberX + totalArea
                        y = numberY + areaHeight

                        if boolValue:
                            # print(f"tolerance found match = {(x, y)} {colour}")
                            return True
                        else:
                            # print(f"tolerance found match = {(x, y)} {colour}")
                            return x, y

            # print('Search done no match, retry!')
            if boolValue:
                return False
            else:
                return 0, 0
    except Exception as e:
        meta = {'Error Info': f"{e}"}
        opts = {'level': 'ERROR', 'app': 'pixelFindColour', 'meta': meta}
        log.info('Click for info!', opts)


def grabPixel(numberX, numberY):
    """ Grabs a pixel colour on a point of the screen."""
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[1])

        return sct_img.pixel(numberX, numberY)


def grabPixels(pixelX, pixelY):
    """ Grabs a pixel colour on a point of the screen."""
    try:
        return ImageGrab.grab().load()[pixelX, pixelY]
    except Exception as e:
        print(f'#ERROR Info {e}\n')  # pass


def humanMove(numberX, numberY, randomMinimum=1, randomMaximum=1, minMove=1, maxMove=1):  # make vetter
    """Humanize moves the mouse cursor to a point on the screen."""

    try:
        moveSpeed = None
        x, y = get_position()
        # randomNumber = randomValue(randomMinimum, randomMaximum, stop0=True)
        randomNumber = randint(randomMinimum, randomMaximum, seed)
        if randomNumber < 1:
            randomNumber = 1

        x2, y2 = (numberX - x) / randomNumber, (numberY - y) / randomNumber

        if randomMaximum <= 1:
            moveSpeed = 0.02
        else:
            for number in range(randomNumber):
                moveSpeed = randfloat(0.02, 0.09, seed)
                # print(moveSpeed)
                offset = randint(minMove, maxMove, seed)
                move(x2 + offset, y2 + offset, False, moveSpeed)

        move(numberX, numberY, duration=moveSpeed)
    except Exception as e:
        print(e)
        meta = {'Error Info': f"{e}"}
        opts = {'level': 'ERROR', 'app': 'humanMove', 'meta': meta}
        log.info('Click for info!', opts)


def humanKeyp(key):
    """ Humanize presses a given key. """
    timeToWaitHold = randfloat(0.047, 0.141, seed)  # 0.032, 0.141 for my mouse
    timeToWaitAfter = randfloat(0.07, 0.15, seed)  # 0.07, 0.15
    kpress(key)
    sleep(timeToWaitHold)  # Delay before I release my mouse button down.
    krelease(key)
    sleep(timeToWaitAfter)


def humanClickerBot(action):
    global timer, fastClick, startTime, afk, sleepTimer, count1, count2, waitClick

    afkTimer = time() - startTime
    chance = randint(0, 100, seed)
    """ Sends a humanize click with the given button. """

    if chance == 22:  # wait time after click is done.
        waitClick = randint(1, 40, seed)
        print("wait to click (anti ban)")
        print(f'Wait Click Amount: {waitClick}')
        count1 += 1

    if chance == 42:  # how many time to rapidly click, am I going to give the bot arthritis? I hope not
        fastClick = randint(1, 50, seed)
        print(f'Fast Click for: {fastClick} clicks (anti ban)')
        print(f'Fast Click Amount: {fastClick}')
        count2 += 1

    if fastClick >= 1:  # rapid click
        # print(f'Fast Click:{fastClick}')
        timeToWait = randfloat(0.032, 0.072, seed)  # set values to your mouse
        fastClick -= 1
    else:
        timeToWait = randfloat(0.032, 0.141, seed)  # delay after you push your click button and releases

    if waitClick >= 1:
        time_to_wait2 = randfloat(0.2, 0.4, seed) # values are set for my mouse
        waitClick -= 1
    else:
        time_to_wait2 = randfloat(0.07, 0.15, seed) # values are set for my mouse

    #  human clicking below
    press(action)
    sleep(timeToWait)
    release(action)
    sleep(time_to_wait2)


## all above is for my brain file that I dont want to release so im copy pasting part of it here


def runTime():
    global forceStop, totalTime, timerLimit, on_off

    start = time()

    while not forceStop:
        totalTime = int(time() - start)

        if totalTime > timerLimit:

            print(
                    f"#Total Minutes = {round((totalTime / 60))}#{strftime('%c')}\n#Total Minutes Limit = {round((timerLimit / 60))}#{strftime('%c')}\n")

            forceStop = True
            on_off = 0
            if forceStop:
                break
        sleep(1)


def toggler():  # pause bot / start bot, he is a smart boy <3
    global on_off
    print("started")
    while True:
        # this is checking if the key is pressed then turn the bot on or off if is is.
        try:
            if is_pressed(key):
                if on_off == 0:

                    on_off = 1
                    print("play")

                elif on_off == 1:
                    print("paused")
                    print(
                            f"\n(Wait to click) Count:{count1}, (Fast Click) Count:{count2} \n(Randomly sleeping) Count:{count3} (Super Randomly sleeping) Count:{count4} \nsmall Afk time:{countTime} Super Afk time:{superCountTime} Total Afk time:{tTime}\n")
                    print(f"Seconds passed: {totalTime}, Min: {totalTime / 60:,.2f}")
                    print(f"Seconds left: {timerLimit - totalTime} Min: {(timerLimit - totalTime) / 60:,.2f}")

                    on_off = 0

                while is_pressed(key):
                    sleep(0.001)
        except Exception as e:  # retard dont break, this tells me why its dumb.
            print(f"#ERROR debug Info {e}\n")
        else:
            sleep(0.01)


def main():
    global on_off

    while not forceStop:
        if on_off == 1:
            if forceStop:
                break

            if pixelFindColour((255, 0, 0), minimapX, minimapY, minimapXMax, minimapYMax, tolerance=20, boolValue=True):

                humanKeyp(fkey)

                xL = randint(logButtonX, logButtonXMax)
                yL = randint(logButtonY, logButtonYMax)

                if humanReactionTime:
                    humanMove(xL, yL, -5, 5, 2, 3)
                else:
                    humanMove(xL, yL)

                humanClickerBot('left')

                start = time()
                while True:
                    colour = grabPixels(logColourLocationX, logColourLocationY)
                    if not pixelMatchesColor(colour, logColour, tolerance=1):  # we have logged out
                        break
                    elif time() - start > 5:  # timeout so it wont get stuck clicking
                        break
                    else:
                        humanClickerBot('left')  # spam click logout


        else:
            # print("what")
            sleep(0.01)
        # print("what2")
    # print("what3")


# why tf would I waste more time coding when I can just multi thead
onoffSwitch = threading.Thread(target=toggler)
onoffSwitch.start()
mainStart = threading.Thread(target=main)
mainStart.start()
start_timer = threading.Thread(target=runTime)
start_timer.start()

'''
5 Hours of running for 
(Wait to click) Count:199, (Fast Click) Count:176 
(Randomly sleeping) Count:30 (Super Randomly sleeping) Count:1 
Total Afk time:586.1495841916534 Super Total Afk time:103.62554360265507'''
