import pygame
import os
import random as rd
import math
import time
import Prey.Deer as Deer
import Predator.Wolf as Wolf
import pygame.freetype
# from graphing import graphPopulation

pygame.init()
pygame.font.init()

WIN_WIDTH = 600
SIM_WIDTH = 600
WIN_HEIGHT = 700
SIM_HEIGHT = 600

PADDING = 10
GLOBAL_ENERGY = 100
STAT_FONT28 = pygame.font.Font((os.path.join("assets","times-new-roman.ttf")), 28)
STAT_FONT14 = pygame.font.Font((os.path.join("assets","times-new-roman.ttf")), 14)
font28 = pygame.font.SysFont("comicsansms", 28)
font14 = pygame.font.SysFont("comicsansms", 14)

SIM_START_TIME = time.time()
activeConsoleMessages = ["00.00: Simulation Started"]
consoleMessages = ["Deer population extinct. Wolves will soon die or migrate elsewhere.",
                   "Deer population is about to go extinct. Wolves will soon die or migrate elsewhere.",
                   "Local wolf population extinct. 2 new wolves arrived from a different territory.",
                   "100 deer added to the ecosystem manually.",
                   "20 wolves added to the ecosystem manually."]

def drawWindow(screen, pack, herd):
    screen.fill((255,255,255))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, SIM_HEIGHT, WIN_WIDTH, WIN_HEIGHT-SIM_HEIGHT))
    for deer in herd:
        deer.draw(screen)
    for wolf in pack:
        wolf.draw(screen)
        # if wolf.target:
        #     pygame.draw.line(screen, (0,0,0), (wolf.x + 8, wolf.y + 8), (wolf.target.x, wolf.target.y))
    # if len(pack) > 0 and len(herd) > 0:
    #     text = STAT_FONT.render("Deer Population: " + str(len(herd)), True, (0, 0, 0))
    #     screen.blit(text, (50, 50))
    #     text = STAT_FONT.render("Wolf Population: " + str(len(pack)), True, (0, 0, 0))
    #     screen.blit(text, (50, 75))
    text = font28.render("Console", True, (255, 255, 255))
    screen.blit(text, (10, SIM_HEIGHT+5))
    text = font28.render("Time elapsed: " + str(round(time.time() - SIM_START_TIME)), True, (255, 255, 255))
    screen.blit(text, (WIN_WIDTH - 180, SIM_HEIGHT + 5))
    messageDisplayHeight = 40
    for consoleMessage in activeConsoleMessages:
        text = font14.render(consoleMessage, True, (255, 255, 255))
        screen.blit(text, (10, SIM_HEIGHT+messageDisplayHeight))
        messageDisplayHeight += 20
    text = font14.render("Wolf Population: " + str(len(pack)), True, (255, 255, 255))
    screen.blit(text, (WIN_WIDTH - 110, SIM_HEIGHT + 40))
    text = font14.render("Deer Population: " + str(len(herd)), True, (255, 255, 255))
    screen.blit(text, (WIN_WIDTH - 110, SIM_HEIGHT + 60))
    text = font14.render("Average Wolf Age: " + str(Wolf.avgWolfAge), True, (255, 255, 255))
    screen.blit(text, (WIN_WIDTH - 110, SIM_HEIGHT + 80))
    pygame.display.update()

def spawnDeer(herd, num):
    for _ in range(num):
        herd.append(Deer.Deer(rd.randint(0, WIN_WIDTH-PADDING), rd.randint(0, SIM_HEIGHT-PADDING)))

def spawnWolf(pack, num):
    for _ in range(num):
        pack.append(Wolf.Wolf(rd.randint(0, WIN_WIDTH-PADDING), rd.randint(0, SIM_HEIGHT-PADDING)))

def checkPopulations(pack, herd):
    global activeConsoleMessages
    if len(herd) == 0:
        addConsoleMessage(consoleMessages[0])
    elif len(herd) <= 10:
        spawnDeer(herd, 50)
        addConsoleMessage(consoleMessages[1])
    if len(pack) < 2:
        spawnWolf(pack, 2)
        addConsoleMessage(consoleMessages[2])


def checkDeadAnimals(pack, herd):
    for deer in herd:
        if not deer.isAlive():
            herd.remove(deer)
    for wolf in pack:
        if not wolf.isAlive():
            pack.remove(wolf)

def checkKillings(pack, herd):
    if len(pack) > 0:
        for wolf in pack:
            if wolf.target:
                if len(herd) > 0:
                    dist = math.sqrt((wolf.x + 8 - wolf.target.x - 4)**2 + (wolf.y + 8 - wolf.target.y - 4)**2)
                    if dist < 20:
                        wolf.eat(wolf.target)
                        wolf.target = None

def moveTargeted(wolf, herd):
    if len(herd) > 0:
        if wolf.target is None:  # select target if not already there
            minDist = math.sqrt((wolf.y - herd[0].y)**2 + (wolf.x - herd[0].x)**2)
            minInd = 0
            for i in range(1, len(herd)):
                dist = math.sqrt((wolf.y - herd[i].y)**2 + (wolf.x - herd[i].x)**2)
                if dist < minDist:
                    minDist = dist
                    minInd = i
            wolf.target = herd[minInd]
        radians = math.atan2(wolf.target.y - wolf.y, wolf.target.x - wolf.x)
        dy = wolf.VEL * math.sin(radians)
        dx = wolf.VEL * math.cos(radians)
        wolf.x += int(dx)
        wolf.y += int(dy)
        wolf.energy -= wolf.FATIGUE
        wolf.checkBounds()
    else:
        wolf.energy -= wolf.IDLE_FATIGUE

def moveTargeted2(deer, pack):
    if len(pack) > 0:
        minDist = math.sqrt((deer.y - pack[0].y) ** 2 + (deer.x - pack[0].x) ** 2)
        minInd = 0
        for i in range(1, len(pack)):
            dist = math.sqrt((deer.y - pack[i].y) ** 2 + (deer.x - pack[i].x) ** 2)
            if dist < minDist:
                minDist = dist
                minInd = i
        nearest = pack[minInd]
        radians = math.atan2(nearest.y - deer.y, nearest.x - deer.x)
        dy = deer.VEL * math.sin(radians)
        dx = deer.VEL * math.cos(radians)
        deer.x -= int(dx)  # running away
        deer.y -= int(dy)
        deer.energy -= deer.FATIGUE
        deer.checkBounds()

def checkActiveConsoleMessages():
    global activeConsoleMessages
    if len(activeConsoleMessages) > 3:
        activeConsoleMessages.pop(0)

def addConsoleMessage(consoleMessage):
    global activeConsoleMessages
    if activeConsoleMessages[-1] != consoleMessage:
        activeConsoleMessages.append(str(round(time.time() - SIM_START_TIME, 2)) + ": " + consoleMessage)

def main():
    running = True
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Wolf-Deer Simulator")
    # numWolves = []
    # frameCounters = []

    spawnDeer(Deer.herd, 100)
    spawnWolf(Wolf.pack, 20)
    frameCounter = 0

    while running:
        frameCounter += 1
        clock.tick(30)

        # event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    spawnDeer(Deer.herd, 100)
                    addConsoleMessage(consoleMessages[3])
                elif event.key == pygame.K_w:
                    spawnWolf(Wolf.pack, 20)
                    addConsoleMessage(consoleMessages[4])

        for wolf in Wolf.pack:
            wolf.grow()
            moveTargeted(wolf, Deer.herd)
        for deer in Deer.herd:
            deer.grow()
            # moveTargeted2(deer, Wolf.pack)
            deer.move()

        checkKillings(Wolf.pack, Deer.herd)
        checkDeadAnimals(Wolf.pack, Deer.herd)
        checkPopulations(Wolf.pack, Deer.herd)
        checkActiveConsoleMessages()

        # Graphing
        # numWolves.append(len(Wolf.pack))
        # frameCounters.append(frameCounter)
        # graphPopulation(numWolves, frameCounter)

        drawWindow(screen, Wolf.pack, Deer.herd)

    pygame.quit()
    quit()

main()