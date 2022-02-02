import pygame
import os
import random as rd
import math
import Prey.Deer as Deer
import Predator.Wolf as Wolf
pygame.init()
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 600
PADDING = 10
GLOBAL_ENERGY = 100
STAT_FONT = pygame.font.Font((os.path.join("assets","statfont.ttf")), 28)

def drawWindow(screen, wolves, herd):
    screen.fill((255,255,255))
    for deer in herd:
        deer.draw(screen)
    for wolf in wolves:
        wolf.draw(screen)
        if wolf.target:
            pygame.draw.line(screen, (0,0,0), (wolf.x + 8, wolf.y + 8), (wolf.target.x + 4, wolf.target.y + 4))
    if len(wolves) > 0:
        text = STAT_FONT.render("Wolf Energy " + str(int(wolves[0].energy)), True, (0, 0, 0))
        screen.blit(text, (50, 50))
        text = STAT_FONT.render("Age: " + str(herd[0].age), True, (0, 0, 0))
        screen.blit(text, (50, 80))
        text = STAT_FONT.render("Mature: " + str(herd[0].mature), True, (0, 0, 0))
        screen.blit(text, (50, 110))
    pygame.display.update()

def spawnDeer(herd, num):
    for _ in range(num):
        herd.append(Deer.Deer(rd.randint(0, WIN_WIDTH-PADDING), rd.randint(0, WIN_HEIGHT-PADDING)))

def spawnWolf(wolves, num):
    for _ in range(num):
        wolves.append(Wolf.Wolf(rd.randint(0, WIN_WIDTH-PADDING), rd.randint(0, WIN_HEIGHT-PADDING)))

def checkDeadAnimals(wolves, herd):
    for deer in herd:
        if not deer.isAlive():
            herd.remove(deer)
    for wolf in wolves:
        if not wolf.isAlive():
            wolves.remove(wolf)

def checkKillings(wolves, herd):
    if len(wolves) > 0:
        for wolf in wolves:
            if wolf.target:
                if len(herd) > 0:
                    dist = math.sqrt((wolf.x + 8 - wolf.target.x - 4)**2 + (wolf.y + 8 - wolf.target.y - 4)**2)
                    if dist < 20:
                        wolf.eat(wolf.target)
                        wolf.target = None

def moveTargeted(wolves, herd):
    if len(herd) > 0:
        for wolf in wolves:
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
            dy = 5 * math.sin(radians)
            dx = 5 * math.cos(radians)
            wolf.x += int(dx)
            wolf.y += int(dy)
            wolf.energy -= wolf.FATIGUE
            wolf.checkBounds()

def main():
    running = True
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    # herd = []
    # wolfList = []
    spawnDeer(Deer.herd, 100)
    spawnWolf(Wolf.wolves, 1)

    # direction = -1

    while running:
        clock.tick(30)

        # event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_w:
            #         direction = 0
            #     if event.key == pygame.K_a:
            #         direction = 2
            #     if event.key == pygame.K_s:
            #         direction = 1
            #     if event.key == pygame.K_d:
            #         direction = 3
            # if event.type == pygame.KEYUP:
            #     direction = -1

        # if len(Wolf.wolves) > 0:
        #     Wolf.wolves[0].moveController(direction)

        for deer in Deer.herd:
            deer.move()
            deer.grow()
        moveTargeted(Wolf.wolves, Deer.herd)
        checkKillings(Wolf.wolves, Deer.herd)
        checkDeadAnimals(Wolf.wolves, Deer.herd)

        for wolf in Wolf.wolves:
            wolf.grow()

        drawWindow(screen, Wolf.wolves, Deer.herd)

    pygame.quit()
    quit()

main()