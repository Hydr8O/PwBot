import pyautogui
import time
import win32gui
from PIL import ImageGrab
import os
from subprocess import Popen
import atexit
import asyncio

recources = 'pictures\\resources\\'

class PwAPI:
    coord = None
    isFlying = False
    farmOnPause = False
    collectingOnPause = False
    mobsKilled = 0
    resourceType = ''
    resourceLevel = ''

    def __init__(self, pathToLauncher, accountLogin, accountPassword, flyHotkey=9):
        self.pathToLauncher = pathToLauncher
        self.accountLogin = accountLogin
        self.accountPassword = accountPassword
        self.flyHotkey = flyHotkey
    
    
    def relogin(self):
        self.exitGame()
        self.enterGame()

    def hideInterface(self):
        pyautogui.hotkey('alt', 'h')

    async def login(self):
        count = 0
        pyautogui.write(self.accountLogin)
        await asyncio.sleep(.3)
        pyautogui.press('tab')
        await asyncio.sleep(.3)
        pyautogui.write(self.accountPassword)
        pyautogui.press('enter')
        await asyncio.sleep(4)
        pyautogui.press('enter')
        await asyncio.sleep(1)
        pyautogui.press('enter')
        print("Logged successfully")

    def exitGame(self):
        os.system("taskkill /f /im  elementclient.exe")

    async def launchGame(self):
        Popen(self.pathToLauncher)
        pyautogui.moveTo(0, 0)
        #self.bringLauncherToFg()
        await asyncio.sleep(5) 
        print ('Searching for the play button')
        playBtn = pyautogui.locateOnScreen('pictures\\playGame.png', confidence=0.7)
        okBtn = pyautogui.locateOnScreen('pictures\\okUpdate.png', confidence=0.7)
        if (okBtn != None):
            await asyncio.sleep(1)
            pyautogui.click(pyautogui.center(okBtn))
            while 1:
                await asyncio.sleep(2)
                playBtn = pyautogui.locateOnScreen('pictures\\playGame.png', confidence=0.7)
                if (playBtn != None):
                    break
        await asyncio.sleep(0.5)
        print ('Clicking on the play button', playBtn)
        pyautogui.click(pyautogui.center(playBtn))
        await asyncio.sleep(2)
        print ('Game has opened')
        await asyncio.sleep(.1)


    async def enterGame(self):
        self.launchGame()
        await asyncio.sleep(8)
        pyautogui.press('esc')
        await asyncio.sleep(1)
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
        if (destination == None):
            return False
        pyautogui.doubleClick(pyautogui.center(destination))
        return True

    async def takeOff(self, seconds):
        pyautogui.keyDown('space')
        await asyncio.sleep(seconds) #Adjusting the height
        pyautogui.keyUp('space')

    async def hasArrived(self): #Works with flying only
        await asyncio.sleep(0.5)
        auto = pyautogui.locateOnScreen('pictures\\auto.png', confidence=0.7)
        print(auto)
        await asyncio.sleep(1)
        if (auto == None):
            return True
        else: 
            return False

    async def goToDestination(self, point):
        self.openCoordinates()
        await asyncio.sleep(.5)
        success = self.clickOnDestinationPoint(point)
        if (not success):
            print('No such point')
            return
        await asyncio.sleep(.5)
        self.closeCoordinates()

    def ensureFlying(self):
        if (not self.isFlying):
            self.useSkill(self.flyHotkey)
            self.isFlying = True


    def chooseResource(self, resourceType, level):
        pathToResource = 'pictures\\resources\\' + resourceType + '\\' + level + '\\'
        return (pathToResource + 'resource.png', pathToResource + 'coordinates.txt')

    async def beforeProgramTerminates(self):
        pwWindow = win32gui.FindWindow(None, '1.4.6 Classic NEW - Твой лучший выбор в 2020 году!')
        win32gui.ShowWindow(pwWindow, 5)
        win32gui.SetForegroundWindow(pwWindow)
        await asyncio.sleep(.1)
        #Anything to do before programm terminates
        if (self.isFlying):
            self.useSkill(self.flyHotkey)

    async def bringLauncherToFg(self):
        await asyncio.sleep(1)
        pwWindow = win32gui.FindWindow(None, '1.4.6 Classic Launcher')
        print(pwWindow)
        win32gui.ShowWindow(pwWindow, 5)
        await asyncio.sleep(.2)
        win32gui.SetForegroundWindow(pwWindow)    

    async def returnToPlace(self):
        self.ensureFlying()
        await asyncio.sleep(1)
        try:
            self.goToDestination('pictures\\point.png')
            pyautogui.moveTo(0, 0)
            while 1:
                if (self.hasArrived()):
                    break
        except:
            pass
    
    async def deleteAllPoints(self):
        deleteBtn = pyautogui.locateOnScreen('pictures\\deleteCoord.png', confidence=0.7)
        pyautogui.click(pyautogui.center(deleteBtn))
        await asyncio.sleep(.1)
        pyautogui.press('enter')

    async def setPoints(self, points):
        self.openCoordinates()
        await asyncio.sleep(.1)
        await self.deleteAllPoints()
        await asyncio.sleep(.1)
        for point in points:
            addCoord = pyautogui.locateOnScreen('pictures\\addCoord.png', confidence=0.7)
            x, y = pyautogui.center(addCoord)
            activateInput = (x - 80, y)
            pyautogui.click(activateInput)
            await self.eraseCoordinates()
            pyautogui.write(point['coordinates'])
            await asyncio.sleep(.1)
            pyautogui.click(pyautogui.center(addCoord))
            pyautogui.write(point['name'])
            pyautogui.press('enter')
        self.closeCoordinates()

    async def eraseCoordinates(self):
        for i in range(7):
                pyautogui.press('backspace')
                await asyncio.sleep(.1)

    def readCoordinates(self, path):
        coordinates = []
        with open(path) as file:
            for line in file:
                coord = line.split(',')[0]
                name = line.split(',')[1].strip()
                coordinates.append({
                    'coordinates': coord,
                    'name': name
                })
        return coordinates

    async def collectResources(self, resourceType, level):
        resourcePicture, coords = self.chooseResource(resourceType, level)

        points = [ 
            recources + 'firstRes.png', 
            recources + 'secondRes.png', 
            recources + 'thirdRes.png', 
            recources + 'forthRes.png', 
            recources + 'fifthRes.png' 
        ]

        coordinates = self.readCoordinates(coords)
        await asyncio.sleep(1)
        await self.setPoints(coordinates)
        pyautogui.moveTo(0, 0)
        self.ensureFlying()
        for point in points:
            print(point)
            await asyncio.sleep(1)
            await self.takeOff(15)
            await self.goToDestination(point)
            pyautogui.moveTo(0, 0)
            while 1:
                print(self.collectingOnPause)
                if self.collectingOnPause == True:
                    return
                if (await self.hasArrived()):
                    await asyncio.sleep(10)
                    self.ensureFlying()
                    self.hideInterface()
                    await asyncio.sleep(13)
                    break
            try:
                resource = pyautogui.locateOnScreen(resourcePicture, confidence=0.6)
                pyautogui.click(pyautogui.center(resource))
                await asyncio.sleep(15)
                self.hideInterface()
                self.ensureFlying()
            except:
                self.hideInterface()
                self.ensureFlying()
        