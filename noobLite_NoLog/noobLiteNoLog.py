# Only change BELOW this Text. Unless you know what you are doing
# v1.0

# *change one of the following to True*

useMouse = False  # will use mouse and right click to stop from logging out. Might be bugged if game not on main monitor
useArrowKey = False  # will use arrow keys to stop from logging out
useTyping = False  # will type to stop from logging out
useFKey = False  # will use 2 fkeys to stop from logging out

whatToType = 'enter', 'a', 'backspace', 'backspace'  # what to type if using useTyping you can edit what you want here, eg "f, backspace" or "shift+s, backspace"
fkeys = 'f2', 'f1'  # what fkeys you want to press *in this order* if using f keys, eg 'f3', 'f2', 'f3'. You want 2 min values

# if your rs name is in the top left of runelite window please write your name here exactly like it is on the game window
name = 'yourNameHERE'

# Only change ABOVE this text. Unless you know what you are doing

import sqlite3
from time import sleep, time
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect, FindWindow, SetForegroundWindow, \
    ShowWindow, GetWindowPlacement, SetActiveWindow
from win32con import SW_SHOW, SW_RESTORE
from os import system
from random import randint, uniform, choice
from keyboard import send, press as kpress, release as krelease, on_release
from mouse import get_position, move, right_click, on_button

forceStop = False
start = None


def makeDB():
    conn = sqlite3.connect(f'settings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE pickChoice
                   (previousPick integer)
                   ''')
    c.execute('''CREATE TABLE fKeys
                       (typeFKeys text)
                       ''')
    c.execute('''CREATE TABLE typeKeys
                           (typeMsgKeys text)
                           ''')
    conn.commit()
    conn.close()


def readUsed():
    sqConn = sqlite3.connect(f'settings.db')
    cursor = sqConn.cursor()
    data = cursor.execute("""SELECT previousPick FROM pickChoice""").fetchall()
    output1 = data[0][0]
    output2 = data[1][0]
    cursor.close()
    return output1, output2


def updateUsed(updateInt, updateText, oldInt, oldText):
    sqConn = sqlite3.connect(f'settings.db')
    cursor = sqConn.cursor()
    cursor.executemany(f""" UPDATE pickChoice 
                        set previousPick = ? 
                        where previousPick = ?""", [(updateInt, oldInt), (updateText, oldText)])
    sqConn.commit()
    cursor.close()


#a, b = readUsed()
# print(a, b)
#updateUsed(0, 'None', a, b)
# a, b = readUsed()
# print(a, b)


def getWP(windowId):
    return GetWindowPlacement(windowId)[1]


def setWindow(windowId):
    # print(windowId)
    if getWP(windowId) == 2:
        ShowWindow(windowId, SW_RESTORE)
    else:
        ShowWindow(windowId, SW_SHOW)
    SetForegroundWindow(windowId)
    SetActiveWindow(windowId)


def timeReset():
    global start
    # mouse_unhook_all()
    # unhook_all()
    currentWindow = GetWindowText(GetForegroundWindow())
    if 'runelite' in currentWindow.lower():
        start = time()
        # print("reset time ", randint(0, 100))
    # else:
    # print("wrong window")

def startUI():
    global useMouse, useArrowKey, useTyping, useFKey
    prePickValue, prePickText = readUsed()

    if prePickValue == 0:
        changeUI()

    picker = None
    try:
        # quality = readQuality()
        # print(f'Made by: Dusty! discord @ "(Dusty) LoseThos#4303" \n\nYour choice is set to (db info here): \n1:Keep your choice as (db info here)\n2:Change your choice\nType Option Here: ')
        # picker = input(f'Made by: Dusty! discord @ "(Dusty) LoseThos#4303" \n\nYour choice is set to (db info here): \nType Number For Option Here: ')
        print('Made by: Dusty! discord @ "(Dusty) LoseThos#4303" \n ')
        picker = input(
                f'Your option choice is set to {prePickText}\n'
                f'1:Keep {prePickText}\n'
                f'2:Change settings/Choice\n'
                f'Type Number Of Option Here: ')
        picker = int(picker)
    except:
        system('cls||clear')
        print(f'\n"{picker}" *is NOT a number please try again*')

        startUI()
    if picker == 1:
        if prePickValue == 1:
            useMouse = True  # will use mouse and right click to stop from logging out. Might be bugged if game not on main monitor
        elif prePickValue == 2:
            useArrowKey = True
        elif prePickValue == 3:
            useTyping = True
        else:
            useFKey = True
        main()

    elif picker == 2:
        system('cls||clear')
        changeUI()
        useArrowKey = True
    else:  # fail safe
        system('cls||clear')
        print(f'\n"{picker}" *is NOT an option to pick from. Please try again*')
        startUI()

def changeUI():
    global useMouse, useArrowKey, useTyping, useFKey
    picker = None
    prePickValue, prePickText = readUsed()

    try:
        # quality = readQuality()
        # print(f'Made by: Dusty! discord @ "(Dusty) LoseThos#4303" \n\nYour choice is set to (db info here): \n1:Keep your choice as (db info here)\n2:Change your choice\nType Option Here: ')
        # picker = input(f'Made by: Dusty! discord @ "(Dusty) LoseThos#4303" \n\nYour choice is set to (db info here): \nType Number For Option Here: ')
        print('Made by: Dusty! discord @ "(Dusty) LoseThos#4303" \n ')
        picker = input(
                f'1:Pick to use mouse *Recommended*\n'
                f'2:Pick to use Arrow keys\n'
                f'3:Pick to use chatbox typing\n'
                f'4:Pick to use F keys\n'
                f'5:Edit what f keys you want to use\n'
                f'6:Edit what to type in chat box\n'
                f'Type Number Of Option Here: ')
        picker = int(picker)
    except:
        system('cls||clear')
        print(f'\n"{picker}" *is NOT a number please try again*')

        changeUI()

    if picker is None:
        # os.system('cls||clear')
        print(f'\n{picker} *is NOT an option to pick from. Please try again*')
        changeUI()

    if picker == 1:
        updateUsed(1, 'using Mouse', prePickValue, prePickText)
        useMouse = True
    elif picker == 2:
        updateUsed(2, 'using Arrow Keys', prePickValue, prePickText)
        useArrowKey = True
    elif picker == 3:
        updateUsed(3, 'using Typing', prePickValue, prePickText)
        useTyping = True
    elif picker == 4:
        updateUsed(4, 'using F Keys', prePickValue, prePickText)
        useFKey = True
    elif picker == 5:
        print("Sorry, does not work atm")
        changeUI()
    elif picker == 6:
        print("Sorry, does not work atm")
        changeUI()
    else:  # fail safe
        system('cls||clear')
        print(f'\n"{picker}" *is NOT an option to pick from. Please try again*')
        changeUI()
    main()


def main():
    global start
    start = time()
    value = -1

    foundName = None
    lastTime = None
    lastX, lastY = 0, 0
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
              'Fix 1): Make sure your name is spelt exactly like in game.\n'
              '2) Go into Runelite plugin settings and turn off "Show display name in title"\n'
              '3) Make sure the game is open and running\n'
              '4) contact Dusty on discord @ "(Dusty) LoseThos#4303"')
        sleep(999999)

    on_button(lambda: timeReset(), buttons=['left', 'right'], types='up')
    on_release(lambda _: timeReset())
    print("Started!")
    start = time()

    while not forceStop:

        sleep(0.01)

        timeValue = float(f'{(time() - start):.1f}')
        if not timeValue == lastTime and timeValue % 1 == 0:
            lastTime = timeValue
            system('cls||clear')
            print('Made by: Dusty! Discord @ "(Dusty) LoseThos#4303"\n')
            print(f"Wait is set to: {(value / 60):.2f} min or {value:.2f} sec")

            if useMouse:
                print(f"Last Moved to [X: {lastX} | Y: {lastY}]")

            print(f"\nAcivation in: {int(value - timeValue)} sec")

        if time() - start > value:
            changeBack = False
            curWindowID = None
            currentWindow = GetWindowText(GetForegroundWindow())

            if 'runelite' not in currentWindow.lower():
                curWindowID = GetForegroundWindow()

                send('shift')  # somehow stops bug where it wont switch windows. I hate windows api dog shit code
                setWindow(winID)

                changeBack = True
            sleep(0.1)
            if useArrowKey:
                print("using a keys")

                keyList = ['up', 'down', 'left', 'right']
                keyList = choice(keyList)

                kpress(keyList)
                sleep(0.02)
                krelease(keyList)
            elif useTyping:  # could combine useTyping and useFKey

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
                lastX, lastY = ranX, ranY
                right_click()
                move(posX, posY, duration=0.02)

            if changeBack:
                setWindow(curWindowID)

            start = time()
            value = uniform(180, 290)  # 3min to 4.9min


startUI()
