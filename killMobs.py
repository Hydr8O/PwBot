import pyautogui
import time
import win32gui as w
from PIL import ImageGrab
from random import randint

pyautogui.FAILSAFE = False
startTimeHeal = time.time()
startTimeFeed = time.time()
startTimeWalk = time.time()
mobsKilled = 0

def relogin():
    pyautogui.press('y')
    while pyautogui.locateOnScreen('/pictures/logPass.png', confidence=0.7) == None:
        time.sleep(.5)
    pyautogui.write('')
    time.sleep(.3)
    pyautogui.press('tab')
    time.sleep(.3)
    pyautogui.write('')
    (x, y, _, __) = pyautogui.locateOnScreen('/pictures/enterGame.png', confidence=0.7)
    pyautogui.click(x=x, y=y)
    while pyautogui.locateOnScreen('/pictures/enter.png', confidence=0.7) == None:
        time.sleep(.5)
    x, y, _, __ = pyautogui.locateOnScreen('/pictures/enter.png', confidence=0.7)
    pyautogui.click(x=x, y=y)
    while pyautogui.locateOnScreen('/pictures/logCheck.png', confidence=0.7) == None:
        time.sleep(.5)
    pyautogui.press('6')
    time.sleep(5)

def collectResources():
    points = [ '/pictures/firstRes.png', '/pictures/secondRes.png','/pictures/thirdRes.png','/pictures/forthRes.png', '/pictures/fifthRes.png' ]
    for point in points:
        print(point)
        time.sleep(1)
        pyautogui.keyDown('space')
        time.sleep(15)
        pyautogui.keyUp('space')
        (x1, y1, _, _) = pyautogui.locateOnScreen('/pictures/coord2.png', confidence=0.6)
        pyautogui.click(x=x1 + 13, y=y1 + 10)
        (x2, y2, _, _) = pyautogui.locateOnScreen(point, confidence=0.7)
        pyautogui.doubleClick(x=x2 + 14, y=y2 + 5)
        time.sleep(1)
        pyautogui.click(x=x1 + 13, y=y1 + 10)
        while 1:
            time.sleep(0.5)
            auto = pyautogui.locateOnScreen('/pictures/auto.png', confidence=0.7)
            time.sleep(.5)
            if (auto == None):
                time.sleep(10)
                pyautogui.press('9')
                time.sleep(13)
                break
        try:
            (x, y, _, __) = pyautogui.locateOnScreen('/pictures/digIron3.png', confidence=0.6)
            pyautogui.click(x + 10, y + 10)
            time.sleep(15)
            pyautogui.press('9')
        except:
            pyautogui.press('9')
            

        

def returnToPlace():
    time.sleep(1)
    location = pyautogui.locateOnScreen('/pictures/coord.png', confidence=0.5)
    try:
        (x, y, width, height) = location
        pyautogui.click(x=(x + 13), y=(y + 10))
        time.sleep(1)
        location = pyautogui.locateOnScreen('/pictures/point.png', confidence=0.6)
        (x2, y2, width, height) = location
        pyautogui.doubleClick(x=x2+20, y=y2+5)
        pyautogui.click(x=(x + 13), y=(y + 10))
        pyautogui.moveTo(x=x-100, y=y-100)
        while 1:
            time.sleep(0.5)
            auto = pyautogui.locateOnScreen('/pictures/autoPath.png', confidence=0.7)
            time.sleep(.5)
            if (auto == None):
                break
    except:
        pass
    
    

def killMobs():
    global mobsKilled
    global startTimeFeed
    global startTimeHeal
    global startTimeWalk
    if (time.time() - startTimeWalk >= 200):
        startTimeWalk = time.time()
        returnToPlace()
            
    time.sleep(.1)
            # full = pyautogui.locateOnScreen('invent.png')
            # if (full == None):
            #     print('full')
            
    pyautogui.press('tab')
    pyautogui.hotkey('alt', '1')
    time.sleep(0.8)
    pyautogui.press('1')
    time.sleep(4)
    pyautogui.press('3')
    time.sleep(1)
            
            
    while 1:
        pyautogui.press('f1')
        if (time.time() - startTimeFeed >= 150):
            startTimeFeed = time.time()
            pyautogui.press('4')
        time.sleep(1)
                
        found = pyautogui.locateOnScreen('/pictures/mob.png', confidence=0.5)
        if (found == None):
            mobsKilled += 1
            print('mobs killed', mobsKilled)
            for i in range(10):
                pyautogui.press('f2')
                time.sleep(.2)
            pyautogui.press('3')
            break

while 1:
    if (w.GetWindowText(w.GetForegroundWindow()) == '1.4.6 Classic NEW - Твой лучший выбор в 2020 году!'):    
        if (pyautogui.locateOnScreen('/pictures/relogMes.png', confidence=0.7) != None):
            relogin()
        else:
            collectResources()

