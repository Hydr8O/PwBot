import discord
from subprocess import Popen
from discord.ext import commands
import pyautogui
import logging
import time
import asyncio
from pwAPI import PwAPI
import secrets

logging.basicConfig(level=logging.INFO)
pyautogui.FAILSAFE = False
PATH_TO_LAUNCHER = 'C:\\Games\\pwClassic\\Launcher.exe'
PATH_TO_ELEMENT = 'C:\\Games\\pwClassic\\element\\elementclient.exe'
LOGIN = secrets.LOGIN
PASSWORD = secrets.PASSWORD
resourceType = ''
resourceLevel = ''


pwApi = PwAPI(PATH_TO_LAUNCHER, LOGIN, PASSWORD, 9)


async def enterGame(channel):
    await pwApi.launchGame()
    await asyncio.sleep(8)
    pyautogui.screenshot('screen.png')
    await channel.send(file=discord.File('screen.png'))
    pyautogui.press('esc')
    await asyncio.sleep(1)
    await pwApi.login()
    pyautogui.screenshot('screen.png')
    await channel.send(file=discord.File('screen.png'))


async def killMobs(startTimeFeed, startTimeHeal, startTimeWalk):
    if (time.time() - startTimeWalk >= 200):
        startTimeWalk = time.time()
        pwApi.returnToPlace()
            
    await asyncio.sleep(.1)
            
    pyautogui.press('tab')
    pyautogui.hotkey('alt', '1')
    await asyncio.sleep(0.8)
    pwApi.useSkill(1)
    await asyncio.sleep(4)
    pwApi.useSkill(3)
    await asyncio.sleep(1)
            
            
    while 1:
        pyautogui.press('f1')
        if (time.time() - startTimeFeed >= 150):
            startTimeFeed = time.time()
            pyautogui.press('4')
        await asyncio.sleep(1)
                
        found = pyautogui.locateOnScreen('pictures\\mob.png', confidence=0.5)
        if (found == None):
            print('mobs killed', pwApi.mobsKilled)
            for i in range(10):
                pyautogui.press('f2')
                await asyncio.sleep(.2)
            pyautogui.press('3')
            return 1

TOKEN = 'NjkyNzU0MjYxMDEyMTE5NTgy.XpXo4g.tUXjZfSxjcKlrhrMeje1iuAfq3c'
client = commands.Bot(command_prefix='.')
@client.event
async def on_ready():
    print ('Connected')

        
@client.command(pass_context=True) # You need to allow to pass the Context object to the command function
async def screen(cntx, *args):
    channel = cntx.message.channel
    await channel.send('Sending a screenshot...')
    print('Sending screenshot')
    channel = cntx.message.channel
    pyautogui.screenshot('screen.png')
    await channel.send(file=discord.File('screen.png'))


@client.command(pass_context=True)
async def launchGame(cntx):
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        await channel.send('Launching the game...')
        try:
            await enterGame(channel)
            await channel.send('The game has launched!')
        except Exception as e:
            print(e)
            await channel.send('Something bad has happened :(')
        
    

@client.command(pass_context=True)
async def exitGame(cntx):
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        await channel.send('Exiting the game...')
        pwApi.exitGame()
        await channel.send('The Game has been closed...')


@client.command(pass_context=True)
async def startFarm(cntx):
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        pwApi.farmOnPause = False
        await channel.send('Farm started.')
        startTimeHeal = time.time()
        startTimeFeed = time.time()
        startTimeWalk = time.time()
        
        while (not pwApi.farmOnPause):
            pwApi.mobsKilled += await killMobs(startTimeHeal, startTimeFeed, startTimeWalk)
        await channel.send('Farm has been stopped.')
        

@client.command(pass_context=True)
async def stopFarm(cntx):
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        pwApi.farmOnPause = True

@client.command(pass_context=True)
async def mobsCount(cntx):
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        await channel.send('Killed ' + str(pwApi.mobsKilled) + ' mobs')

@client.command(pass_context=True)
async def test(cntx):
    channel = cntx.message.channel
    print(isinstance(channel, discord.DMChannel))        

@client.command(pass_context=True)
async def collect(cntx):
    pwApi.collectingOnPause = False
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        if (resourceLevel == '' or resourceType == ''):
            await channel.send('What kind of resources do you want to collect?')
        else:
            while not pwApi.collectingOnPause:
                await pwApi.collectResources(resourceType, resourceLevel)

@client.command(pass_context=True)
async def stopCollect(cntx):
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        pwApi.collectingOnPause = True
        await channel.send('Collecting was paused')
        

@client.command(pass_context=True)
async def iron3(cntx):
    global resourceLevel, resourceType
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        resourceType = 'iron'
        resourceLevel = '3'
        await channel.send('You have specified to collect ' + resourceType + ' ' + 'level ' + resourceLevel)

@client.command(pass_context=True)
async def currentRes(cntx):
    channel = cntx.message.channel
    if (isinstance(channel, discord.DMChannel)):
        if (resourceLevel == '' or resourceType == ''):
            await channel.send("Resource isn't set")  
        else:
            await channel.send(resourceType + ' level ' + resourceLevel)
client.run(TOKEN)



