# Only change BELOW this Text. Unless you know what you are doing
# v1.0

# *change one of the following to True*

useMouse = True  # will use mouse and right click to stop from logging out. Might be bugged if game not on main monitor
useArrow = False  # will use arrow keys to stop from logging out
useType = False  # will type to stop from logging out
useFKey = False  # will use 2 fkeys to stop from logging out

whatToType = 'enter', 'a', 'backspace', 'backspace'  # what to type if using useType you can edit what you want here, eg "f, backspace" or "shift+s, backspace"
fkeys = 'f2', 'f1'  # what fkeys you want to press *in this order* if using f keys, eg 'f3', 'f2', 'f3'. You want 2 min values

# if your rs name is in the top left of runelite window please write your name here exactly like it is on the game window
name = 'yourNameHERE'

# Only change ABOVE this text. Unless you know what you are doing


from time import sleep, time
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect, FindWindow, SetForegroundWindow, \
    ShowWindow, GetWindowPlacement, SetActiveWindow
from win32con import SW_SHOW, SW_RESTORE
from random import randint, uniform, choice
from keyboard import send, press as kpress, release as krelease, on_release, unhook_all
from mouse import get_position, move, right_click, on_button, unhook_all as mouse_unhook_all

forceStop = False
start = None


def getWP(windowId):
    return GetWindowPlacement(windowId)[1]


def setWindow(windowId):
    #print(windowId)
    if getWP(windowId) == 2:
        ShowWindow(windowId, SW_RESTORE)
    else:
        ShowWindow(windowId, SW_SHOW)
    SetForegroundWindow(windowId)
    SetActiveWindow(windowId)


def timeReset():
    global start
    mouse_unhook_all()
    unhook_all()
    currentWindow = GetWindowText(GetForegroundWindow())
    if 'runelite' in currentWindow.lower():
        start = time()
        # print("reset time")
    # else:
    # print("wrong window")


def main():
    global start
    start = time()
    value = uniform(180, 270)  # 3min to 4.5min
    value = 2

    foundName = None

    winID1 = FindWindow(None, f"RuneLite")
    winID2 = FindWindow(None, f"RuneLite - {name}")
    winID = None

    if winID1 != 0:
        foundName = 'RuneLite'
        winID = winID1
    elif winID2 != 0:
        foundName = f"RuneLite - {name}"
        winID = winID2
    else:
        print("Could not find Runelite!\n"
                        "Fix 1): Make sure your name is spelt exactly like in game.\n"
                        '2) Go into Runelite plugin settings and turn off "Show display name in title"\n'
                        '3) Make sure the game is open and running\n'
                        '4) contact Dusty on discord @ "(Dusty) LoseThos#4303"')
        sleep(999999)

    print("started")
    start = time()
    while not forceStop:
        # while True:

        on_button(lambda: timeReset(), buttons=['left', 'right'], types='up')
        on_release(lambda _: timeReset())
        sleep(0.01)

        if time() - start > value:
            changeBack = False
            curWindowID = None
            currentWindow = GetWindowText(GetForegroundWindow())

            if 'runelite' not in currentWindow.lower():
                curWindowID = GetForegroundWindow()

                send('shift')  # somehow stops bug where it wont switch windows. I hate windows api dog shit code
                setWindow(winID)

                changeBack = True

            if useArrow:
                keyList = ['up', 'down', 'left', 'right']
                keyList = choice(keyList)

                kpress(keyList)
                sleep(0.02)
                krelease(keyList)
            elif useType:  # could combine useType and useFKey
                for i in whatToType:
                    kpress(i)
                    sleep(0.02)
                    krelease(i)
            elif useFKey:
                for i in fkeys:
                    kpress(i)
                    sleep(0.02)
                    krelease(i)
            else:
                windowTitle = FindWindow(None, f"{foundName}")
                x, y, xMax, yMax = GetWindowRect(windowTitle)

                removeXMax = round(xMax * 20 / 100)
                removeX = round(x * 20 / 100)
                addY = round(yMax * 2 / 100)
                ranXMax = (xMax - removeXMax) + removeX
                ranX = randint(x, ranXMax)
                ranY = randint(y + addY, yMax)

                # print(f'x, y, xMax, yMax = {x, y, xMax, yMax}')
                # print(f'removeX, addY = {removeX, addY}')
                # print(f'ranxMax = {ranxMax}')

                posX, posY = get_position()
                move(ranX, ranY, duration=0.02)
                right_click()
                move(posX, posY, duration=0.02)

            if changeBack:
                setWindow(curWindowID)

            start = time()
            value = uniform(180, 300)  # 3min to 4.5min


main()
