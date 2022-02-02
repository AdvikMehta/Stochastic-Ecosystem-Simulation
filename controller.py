import pygame
import random as rd
import Prey.Deer as Deer
import Predator.Wolf as Wolf

WIN_WIDTH = 600
WIN_HEIGHT = 600
PADDING = 10
GLOBAL_ENERGY = 100

def drawWindow(screen, wolfList, deerList):
    screen.fill((255,255,255))
    for deer in deerList:
        deer.draw(screen)
    for wolf in wolfList:
        wolf.draw(screen)
    pygame.display.update()

def spawnDeer(deerList, num):
    for _ in range(num):
        deerList.append(Deer.Deer(rd.randint(0, WIN_WIDTH-PADDING), rd.randint(0, WIN_HEIGHT-PADDING)))

def spawnWolf(wolfList, num):
    for _ in range(num):
        wolfList.append(Wolf.Wolf(rd.randint(0, WIN_WIDTH-PADDING), rd.randint(0, WIN_HEIGHT-PADDING)))

def checkDeadAnimals(wolfList, deerList):
    for deer in deerList:
        if not deer.isAlive():
            deerList.remove(deer)
    for wolf in wolfList:
        if not wolf.isAlive():
            wolfList.remove(wolf)

def checkKillings(wolfList, deerList):
    if len(wolfList) > 0:
        wolfMask = wolfList[0].getMask()
        for deer in deerList:
            deerMask = deer.getMask()
            offset = (wolfList[0].x - deer.x, wolfList[0].y - deer.y)
            point = wolfMask.overlap(deerMask, offset)
            if point:
                deer.isEaten()

def main():
    running = True
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    deerList = []
    wolfList = []
    spawnDeer(deerList, 10)
    spawnWolf(wolfList, 1)

    direction = -1

    while running:
        clock.tick(30)

        # event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    direction = 0
                if event.key == pygame.K_a:
                    direction = 2
                if event.key == pygame.K_s:
                    direction = 1
                if event.key == pygame.K_d:
                    direction = 3
            if event.type == pygame.KEYUP:
                direction = -1

        if len(wolfList) > 0:
            wolfList[0].moveController(direction)
        for deer in deerList:
            deer.move()

        checkKillings(wolfList, deerList)
        checkDeadAnimals(wolfList, deerList)

        drawWindow(screen, wolfList, deerList)

    pygame.quit()
    quit()

main()