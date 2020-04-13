import pyautogui
import time
import win32gui
from PIL import ImageGrab
import os
from subprocess import Popen
import atexit


class PwAPI:
    coord = None
    isFlying = False
    def __init__(self, pathToLauncher, accountLogin, accountPassword, flyHotkey=9):
        self.pathToLauncher = pathToLauncher
        self.accountLogin = accountLogin
        self.accountPassword = accountPassword
        self.flyHotkey = flyHotkey
        atexit.register(self.__beforeProgramTerminates)
    
    
    def relogin(self):
        self.exitGame()
        self.enterGame()

    def hideInterface(self):
        pyautogui.hotkey('alt', 'h')

    def login(self):
        pyautogui.write(self.accountLogin)
        time.sleep(.3)
        pyautogui.press('tab')
        time.sleep(.3)
        pyautogui.write(self.accountPassword)
        pyautogui.press('enter')
        time.sleep(4)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        print("Login check...")
        while pyautogui.locateOnScreen('pictures\\logCheck.png', confidence=0.7) == None:
            time.sleep(.5)
        print("Logged successfully")

    def exitGame(self):
        os.system("taskkill /f /im  elementclient.exe")

    def launchGame(self):
        Popen(self.pathToLauncher)
        pyautogui.moveTo(0, 0)
        time.sleep(3) 
        playBtn = pyautogui.locateOnScreen('pictures\\playGame.png', confidence=0.8)
        okBtn = pyautogui.locateOnScreen('pictures\\okUpdate.png', confidence=0.8)
        if (okBtn != None):
            time.sleep(1)
            pyautogui.click(pyautogui.center(okBtn))
            while 1:
                time.sleep(2)
                playBtn = pyautogui.locateOnScreen('pictures\\playGame.png', confidence=0.8)
                if (playBtn != None):
                    break
        pyautogui.click(pyautogui.center(playBtn))
        time.sleep(2)
        print ('Game has opened')


    def enterGame(self):
        self.launchGame()
        time.sleep(6)
        pyautogui.press('esc')
        time.sleep(1)
        self.login()

    def useSkill(self, numberOfSkill, f=False):
        skillHotKeys = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        skillHotKeysF = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8']
        if (numberOfSkill == self.flyHotkey and self.isFlying == False):
            self.isFlying = True
        elif (numberOfSkill == self.flyHotkey and self.isFlying == True):
            self.isFlying = False

        if (f):
            pyautogui.press(skillHotKeysF[numberOfSkill - 1])
        else:
            pyautogui.press(skillHotKeys[numberOfSkill - 1])

    def openCoordinates(self):
        self.coord = pyautogui.locateOnScreen('pictures\\coord2.png', confidence=0.6)
        pyautogui.click(pyautogui.center(self.coord))
    
    def closeCoordinates(self):
        if (self.coord != None):
            pyautogui.click(pyautogui.center(self.coord))

    def clickOnDestinationPoint(self, point):
        destination = pyautogui.locateOnScreen(point, confidence=0.7)
        pyautogui.doubleClick(pyautogui.center(destination))

    def takeOff(self, seconds):
        pyautogui.keyDown('space')
        time.sleep(seconds) #Adjusting the height
        pyautogui.keyUp('space')

    def hasArrived(self): #Works with flying only
        time.sleep(0.5)
        auto = pyautogui.locateOnScreen('pictures\\auto.png', confidence=0.7)
        print(auto)
        time.sleep(1)
        if (auto == None):
            return True
        else: 
            return False

    def goToDestination(self, point):
        self.openCoordinates()
        time.sleep(.5)
        self.clickOnDestinationPoint(point)
        self.closeCoordinates()

    def ensureFlying(self):
        if (not self.isFlying):
            self.useSkill(self.flyHotkey)
            self.isFlying = True

    def __beforeProgramTerminates(self):
        pwWindow = win32gui.FindWindow(None, '1.4.6 Classic NEW - Твой лучший выбор в 2020 году!')
        win32gui.ShowWindow(pwWindow, 5)
        win32gui.SetForegroundWindow(pwWindow)
        time.sleep(.1)
        #Anything to go before programm terminates
        if (self.isFlying):
            self.useSkill(self.flyHotkey)

        

        