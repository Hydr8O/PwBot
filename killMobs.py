import pyautogui
import time
from pwAPI import PwAPI
import win32gui as w
from PIL import ImageGrab
from random import randint
import subprocess
import os
import secrets

PATH_TO_LAUNCHER = 'C:\\Games\\pwClassic\\Launcher.exe'
PATH_TO_ELEMENT = 'C:\\Games\\pwClassic\\element\\elementclient.exe'
LOGIN = secrets.LOGIN
PASSWORD = secrets.PASSWORD
FLY_HOTKEY = 9

pwApi = PwAPI(PATH_TO_LAUNCHER, LOGIN, PASSWORD, FLY_HOTKEY)

pyautogui.FAILSAFE = False
startTimeHeal = time.time()
startTimeFeed = time.time()
startTimeWalk = time.time()
mobsKilled = 0
    

def collectResources():
    points = [ 'pictures\\firstRes.png', 'pictures\\secondRes.png','pictures\\thirdRes.png','pictures\\forthRes.png', 'pictures\\fifthRes.png' ]
    for point in points:
        print(point)
        time.sleep(1)
        pwApi.takeOff(15)
        pwApi.openCoordinates()
        pwApi.goToDestination(point)
        time.sleep(1)
        pwApi.closeCoordinates()
        time.sleep(.2)
        pyautogui.moveTo(0, 0)
        while 1:
            if (pwApi.hasArrived()):
                time.sleep(10)
                pwApi.useSkill(9)
                pwApi.hideInterface()
                time.sleep(13)
                break
        try:
            recource = pyautogui.locateOnScreen('pictures\\digIron3.png', confidence=0.6)
            pyautogui.click(pyautogui.center(recource))
            time.sleep(15)
            pwApi.hideInterface()
            pwApi.useSkill(9)
        except:
            pwApi.hideInterface()
            pwApi.useSkill(9)
            

       

def returnToPlace():
    pwApi.ensureFlying()
    time.sleep(1)
    try:
        pwApi.goToDestination('pictures\\point.png')
        pyautogui.moveTo(0, 0)
        while 1:
            if (pwApi.hasArrived()):
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
                
        found = pyautogui.locateOnScreen('pictures\\mob.png', confidence=0.5)
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
        if (pyautogui.locateOnScreen('pictures\\relogMes.png', confidence=0.7) != None):
            pwApi.relogin()
        else:
            returnToPlace()
        

