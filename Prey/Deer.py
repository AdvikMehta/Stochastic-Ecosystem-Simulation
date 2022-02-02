import pygame
import os
import random as rd

DEER_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets","deer.png")),  (8, 8))

class Deer:
    MAX_VEL = 5
    FATIGUE = 0.1
    MAX_MOVE_TIME = 30  # frames

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100
        self.hunger = 0
        self.age = 0
        self.health = 0
        self.alive = True
        self.moveTime = self.MAX_MOVE_TIME
        self.vel = (0,0)

    def move(self):
        if self.moveTime < self.MAX_MOVE_TIME:
            self.x += self.vel[0]
            self.y += self.vel[1]
            self.moveTime += 1
            self.energy -= self.FATIGUE
        else:  # 1 frame stop and change dir
            self.moveTime = 0
            self.vel = (rd.randint(-5, 5), rd.randint(-5, 5))
        self.checkBounds()

    def checkBounds(self):
        if self.x < 0 or self.x > 600:
            self.vel = (-self.vel[0], self.vel[1])
        if self.y < 0 or self.y > 600:
            self.vel = (self.vel[0], -self.vel[1])

    def isEaten(self):
        self.energy = 0
        self.alive = False

    def draw(self, screen):
        screen.blit(DEER_IMG, (self.x, self.y))

    def isAlive(self):
        return self.alive

    def getMask(self):
        return pygame.mask.from_surface(DEER_IMG)