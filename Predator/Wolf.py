import pygame
import os

WOLF_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets","wolf.png")),  (16, 16))

class Wolf:
    VEL = 5
    FATIGUE = 0.5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100
        self.hunger = 0
        self.age = 0
        self.health = 0
        self.alive = True

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.energy -= self.FATIGUE
        if self.energy < 0:
            self.alive = False
        self.checkBounds()

    def moveController(self, direction):
        if direction == -1:
            return
        if direction == 0:  # up
            self.y -= self.VEL
        elif direction == 1:  # down
            self.y += self.VEL
        elif direction == 2:  # left
            self.x -= self.VEL
        else:  # right
            self.x += self.VEL
        self.energy -= self.FATIGUE
        if self.energy < 0:
            self.alive = False
        self.checkBounds()

    def checkBounds(self):
        if self.x < 0:
            self.x = 0
        if self.x > 600-WOLF_IMG.get_width():
            self.x = 600-WOLF_IMG.get_width()
        if self.y < 0:
            self.y = 0
        if self.y > 600-WOLF_IMG.get_height():
            self.y = 600-WOLF_IMG.get_height()

    def eat(self, prey):
        self.hunger = 0
        self.energy = 100 if self.energy > 30 else self.energy + 70
        prey.isEaten()

    def kill(self):
        self.energy = 0
        self.alive = False

    def draw(self, screen):
        screen.blit(WOLF_IMG, (self.x, self.y))

    def isAlive(self):
        return self.alive

    def getMask(self):
        return pygame.mask.from_surface(WOLF_IMG)