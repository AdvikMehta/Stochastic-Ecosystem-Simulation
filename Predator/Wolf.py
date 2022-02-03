import pygame
import os
import time
import random

WOLF_IMG = pygame.transform.scale(pygame.image.load(os.path.join("assets","wolf.png")),  (16, 16))
pack = []

class Wolf:
    VEL = 5.5  # velocity - 50-60 kmph
    FATIGUE = 0.5  # energy cost for moving
    IDLE_FATIGUE = 0.3  # energy cost if not moving for food
    MAX_AGE = 15  # maximum life of a wolf
    MAX_HUNGER = 1  # maximum seconds a wolf can go without eating
    MATURITY_AGE = 3  # age of maturity
    MIN_LITTER_SIZE = 1  # minimum size of litter
    MAX_LITTER_SIZE = 2  # maximum size of litter
    BIRTH_INTERVAL = 1  # inrerval between two litters
    REPRODUCTION_PROXIMITY = 100  # spawn offspring within this radius
    REPRODUCTION_THRESHOLD = 90  # minimum energy required to reproduce
    REPRODUCTION_ENERGY = 40  # energy required to reproduce

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100
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
        self.energy = 100 if self.energy > 30 else self.energy + 70
        prey.isEaten()

    def kill(self):
        self.energy = 0
        self.alive = False

    def grow(self):
        self.age = time.time() - self.spawn_time
        self.timeSinceLastBirth = time.time() - self.birthTime
        self.hunger = time.time() - self.lastMealTime

        if self.age > self.MAX_AGE or self.energy < 0 or self.hunger > self.MAX_HUNGER:
            self.kill()
        elif self.age > self.MATURITY_AGE:
            self.mature = True
        if self.mature and self.timeSinceLastBirth > self.BIRTH_INTERVAL and self.energy > 90:
            self.reproduce()

    def reproduce(self):
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