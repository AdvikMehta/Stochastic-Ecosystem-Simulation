import pygame
import os
import random
import time

DEER_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets","deer.png")),  (8, 8))
PADDING = 10
MAX_POPULATION = 1000
herd = []

class Deer:
    VEL = 3  # velocity
    FATIGUE = 0.5  # energy cost for moving
    MAX_MOVE_TIME = 30  # number of frames to move in random dir
    MAX_AGE = 2  # maximum life of a deer
    MATURITY_AGE = 2  # age of maturity in secs
    MIN_LITTER_SIZE = 3  # minimum size of litter
    MAX_LITTER_SIZE = 5  # maximum size of litter
    BIRTH_INTERVAL = 0.3  # inrerval between two litters
    REPRODUCTION_PROXIMITY = 100  # spawn offspring within this radius
    REPRODUCTION_THRESHOLD = 90  # energy required to reproduce
    REPRODUCTION_ENERGY = 40  # energy required to reproduce

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100
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
            if (self.x <= PADDING and self.vel[0] < 0) or (self.x >= 600-PADDING and self.vel[0] > 0):
                self.vel = -self.vel[0], self.vel[1]
            if (self.y == PADDING and self.vel[1] < 0) or (self.y >= 600-PADDING and self.vel[1] > 0):
                self.vel = self.vel[0], -self.vel[1]
            self.x += self.vel[0]
            self.y += self.vel[1]
            self.moveTime += 1
            self.energy -= self.FATIGUE
        else:  # 1 frame stop and change dir
            self.moveTime = 0
            self.vel = (random.randint(-5, 5), random.randint(-5, 5))
        self.checkBounds()

    def checkBounds(self):
        if self.x < PADDING:
            self.x = PADDING + 1
        if self.x > 600 - PADDING:
            self.x = 600 - PADDING - 1
        if self.y < PADDING:
            self.y = PADDING + 1
        if self.y > 600 - PADDING:
            self.y = 600 - PADDING - 1

    def isEaten(self):
        self.energy = 0
        self.alive = False

    def grow(self):
        self.age = time.time() - self.spawn_time
        self.timeSinceLastBirth = time.time() - self.birthTime
        if self.age > self.MAX_AGE:
            self.isEaten()
        if self.age > self.MATURITY_AGE:
            self.mature = True
        if self.mature and self.timeSinceLastBirth > self.BIRTH_INTERVAL and len(herd) < MAX_POPULATION:
            self.reproduce()

    def reproduce(self):
        self.birthTime = time.time()
        self.energy -= self.REPRODUCTION_ENERGY
        self.timeSinceLastBirth = 0
        litterSize = random.randint(1, self.MAX_LITTER_SIZE)
        for _ in range(litterSize):
            randX = random.randint(-self.REPRODUCTION_PROXIMITY, self.REPRODUCTION_PROXIMITY)
            randY = random.randint(-self.REPRODUCTION_PROXIMITY, self.REPRODUCTION_PROXIMITY)
            if self.x + randX < PADDING or self.x + randX > 600 - PADDING:
                randX = 0
            if self.y + randY < PADDING or self.y + randY > 600 - PADDING:
                randY = 0
            herd.append(Deer(self.x + randX, self.y + randY))

    def draw(self, screen):
        pygame.draw.circle(screen, (51,204,255), (self.x, self.y), 4)

    def isAlive(self):
        return self.alive

    def getMask(self):
        return pygame.mask.from_surface(DEER_IMG)