import pyautogui
import time
import win32gui as w
from PIL import ImageGrab
import pytesseract

def goToQuest(questCompleted):
    time.sleep(1)
    pyautogui.press('q')
    
    quest = pyautogui.locateOnScreen('MainQuest.png')
    (left, top, width, height) = quest
    pyautogui.click(x=left + 90, y=top + 50)
    time.sleep(.5)
    locationToGoKill = pyautogui.locateOnScreen('killQuest.png', confidence=0.8)
    locationToGoNpc = pyautogui.locateOnScreen('npcQuest.png')
    print(locationToGoKill, locationToGoNpc)
    if (locationToGoKill == None and locationToGoNpc == None):
        pyautogui.click(x=left + 90, y=top + 30)

    if (questCompleted):
        locationToGo = pyautogui.locateOnScreen('npcQuest.png')
        (left, top, width, height) = locationToGo
        pyautogui.click(x=left + 200, y=top + 5)
        time.sleep(.3)
        pyautogui.press('q')
        return (None, None)
    else:
        locationToGo = pyautogui.locateOnScreen('killQuest.png', confidence=0.8)
    
    if (locationToGo == None):
        locationToGo = pyautogui.locateOnScreen('npcQuest.png')
        (left, top, width, height) = locationToGo
        numberOfMobs = (None, None)
    else:
        (left, top, width, height) = locationToGo
        print(locationToGo)
        img = ImageGrab.grab((left + width, top - 5, left + width + 180, top + height))
        img = img.convert('L')
        img.save('test.png')
        name = pytesseract.image_to_string(img, config='--psm 7 digits')
        print('name', name)
        mobsNeeded = int(list(name.replace('.', ''))[1])
        mobsKilled = int(list(name.replace('.', ''))[0])
        numberOfMobs = (mobsKilled, mobsNeeded)
    
    pyautogui.click(x=left + 200, y=top + 5)
    time.sleep(.3)
    pyautogui.press('q')
    return numberOfMobs
    
def hasReachedDestination():
    while 1:
        time.sleep(1)
        if (pyautogui.locateOnScreen('autoPath.png', confidence=0.6) == None):
            print('Reached quest point')
            break

questCompleted = False
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
while 1:
    if (w.GetWindowText(w.GetForegroundWindow()) == '1.4.6 Classic NEW - Твой лучший выбор в 2020 году!'):
        mobsKilled = 0
        mobsNeeded = 0
        (mobsKilled, mobsNeeded) = goToQuest(questCompleted)
        if (mobsNeeded == None):
            hasReachedDestination()
            location = pyautogui.locateOnScreen('passQuest.png', confidence=0.9)
            (left, top, width, height) = location
            pyautogui.click(x=left + 100, y=top + 15)
            break
        questCompleted = False
        print('Going to the quest')
        hasReachedDestination()
        while 1:
            if (questCompleted):
                break
            pyautogui.press('tab')
            img = ImageGrab.grab((912, 65, 1078, 80))
            img = img.convert('L')
            img.save('currentMob.png')
            name = pytesseract.image_to_string(img, config='--psm 7', lang='rus')
            print('current', name)
            pyautogui.press('1')
            time.sleep(1.4)
            while 1:
                pyautogui.press('f1')
                time.sleep(1.5)
                found = pyautogui.locateOnScreen('mob.png', confidence=0.5)
                if (found == None):
                    mobsKilled += 1
                    print('mobs killed', mobsKilled)
                    print('number needed', mobsNeeded)
                    pyautogui.keyDown('f2')
                    time.sleep(5)
                    pyautogui.keyUp('f2')
                    if (mobsKilled >= mobsNeeded):
                        print('completed')
                        questCompleted = True
                        numberOfMobs = 0
                    break

    