import pygame
import os
import time
import random

WOLF_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets","wolf.png")),  (16, 16))
MAX_POPULATION = 300
pack = []
avgWolfAge = 0
maxWolfAge = 0
totalWolvesExisted = 0

class Wolf:
    MAX_ENERGY = 100  # total energy of a wolf
    VEL = 6  # velocity - 50-60 kmph
    FATIGUE = 1.5  # energy cost for moving
    IDLE_FATIGUE = 0.3  # energy cost if not moving for food
    MAX_AGE = 20  # maximum life of a wolf
    MAX_HUNGER = 1  # maximum seconds a wolf can go without eating
    EAT_ENERGY = 70  # energy gained from eating prey
    MATURITY_AGE = 4  # age of maturity
    MIN_LITTER_SIZE = 1  # minimum size of litter
    MAX_LITTER_SIZE = 2  # maximum size of litter
    BIRTH_INTERVAL = 5  # inrerval between two litters
    REPRODUCTION_PROXIMITY = 100  # spawn offspring within this radius
    REPRODUCTION_THRESHOLD = 95  # minimum energy required to reproduce
    REPRODUCTION_ENERGY = 40  # energy loss during reproduction

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = self.MAX_ENERGY
        self.hunger = 0
        self.gender = random.randint(0, 1)  # 0 for male, 1 for female
        self.age = 0  # in secs
        self.health = 0
        self.alive = True
        self.mature = False
        self.spawn_time = time.time()
        self.lastMealTime = self.spawn_time
        self.birthTime = self.spawn_time
        self.timeSinceLastBirth = 0
        self.vel = (0, 0)
        self.target = None

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
        self.lastMealTime = time.time()
        self.energy = 100 if self.energy > (100 - self.EAT_ENERGY) else self.energy + self.EAT_ENERGY
        prey.isEaten()

    def kill(self):
        global totalWolvesExisted, avgWolfAge, maxWolfAge
        self.energy = 0
        self.alive = False
        totalWolvesExisted += 1
        avgWolfAge = ((avgWolfAge*(totalWolvesExisted-1)) + self.age) / totalWolvesExisted
        maxWolfAge = max(self.age, maxWolfAge)

    def grow(self):
        self.age = time.time() - self.spawn_time
        self.timeSinceLastBirth = time.time() - self.birthTime
        self.hunger = time.time() - self.lastMealTime

        if self.age > self.MAX_AGE or self.energy < 0 or self.hunger > self.MAX_HUNGER:
            self.kill()
        elif self.age > self.MATURITY_AGE:
            self.mature = True
        if self.mature and self.timeSinceLastBirth > self.BIRTH_INTERVAL and self.energy > self.REPRODUCTION_THRESHOLD and len(pack) < MAX_POPULATION:
            self.reproduce()

    def reproduce(self):
        global totalWolvesExisted
        self.birthTime = time.time()
        self.energy -= self.REPRODUCTION_ENERGY
        self.timeSinceLastBirth = 0
        litterSize = random.randint(self.MIN_LITTER_SIZE, self.MAX_LITTER_SIZE)
        for _ in range(litterSize):
            pack.append(Wolf(self.x + random.randint(-self.REPRODUCTION_PROXIMITY, self.REPRODUCTION_PROXIMITY),
                            self.y + random.randint(-self.REPRODUCTION_PROXIMITY, self.REPRODUCTION_PROXIMITY)))

    def draw(self, screen):
        screen.blit(WOLF_IMG, (self.x, self.y))

    def isAlive(self):
        return self.alive

    def getMask(self):
        return pygame.mask.from_surface(WOLF_IMG)