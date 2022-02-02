import pygame
import os
import random
import time

DEER_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets","deer.png")),  (8, 8))
PADDING = 10
herd = []

class Deer:
    MAX_VEL = 5  # velocity
    FATIGUE = 0.5  # energy cost for moving
    MAX_MOVE_TIME = 30  # number of frames to move in random dir
    MAX_AGE = 12  # maximum life of a deer
    MAX_HUNGER = 3  # maximum seconds a wolf can go without eating
    MATURITY_AGE = 7  # age of maturity in secs
    BIRTH_INTERVAL = 2  # inrerval between two litters
    REPRODUCTION_PROXIMITY = 100  # spawn offspring within this radius
    REPRODUCTION_THRESHOLD = 90  # energy required to reproduce

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100
        # self.hunger = 0
        self.age = 0
        self.health = 0
        self.alive = True
        self.mature = False
        self.moveTime = self.MAX_MOVE_TIME
        self.vel = (0,0)
        self.spawn_time = time.time()
        self.birthTime = self.spawn_time
        self.timeSinceLastBirth = 0

    def move(self):
        if self.moveTime < self.MAX_MOVE_TIME:
            self.x += self.vel[0]
            self.y += self.vel[1]
            self.moveTime += 1
            self.energy -= self.FATIGUE
        else:  # 1 frame stop and change dir
            self.moveTime = 0
            self.vel = (random.randint(-5, 5), random.randint(-5, 5))
        self.checkBounds()

    def checkBounds(self):
        if self.x < 0:
            self.x = 0
        if self.x > 600 - DEER_IMG.get_width():
            self.x = 600 - DEER_IMG.get_width()
        if self.y < 0:
            self.y = 0
        if self.y > 600 - DEER_IMG.get_height():
            self.y = 600 - DEER_IMG.get_height()

    def isEaten(self):
        self.energy = 0
        self.alive = False

    def grow(self):
        self.age = time.time() - self.spawn_time
        self.timeSinceLastBirth = time.time() - self.birthTime
        if self.age > self.MAX_AGE:
            self.isEaten()
            herd.remove(self)
        if self.age > self.MATURITY_AGE:
            self.mature = True
        if self.mature and self.timeSinceLastBirth > self.BIRTH_INTERVAL:
            self.reproduce()

    def reproduce(self):
        self.birthTime = time.time()
        self.timeSinceLastBirth = 0
        litterSize = random.randint(1, 2)
        for _ in range(litterSize):
            randX = random.randint(-self.REPRODUCTION_PROXIMITY, self.REPRODUCTION_PROXIMITY)
            randY = random.randint(-self.REPRODUCTION_PROXIMITY, self.REPRODUCTION_PROXIMITY)
            if self.x + randX < 0:
                randX = 0
            elif self.x + randX > 600 - PADDING:
                randX = 0
            if self.y + randY < 0:
                randY = 0
            elif self.y + randY > 600 - PADDING:
                randY = 0
            herd.append(Deer(self.x + randX, self.y + randY))

    def draw(self, screen):
        screen.blit(DEER_IMG, (self.x, self.y))

    def isAlive(self):
        return self.alive

    def getMask(self):
        return pygame.mask.from_surface(DEER_IMG)