# Inimigos do jogo
import pygame as pg
from random import randint

from ..tools import load_image
from ..constants import ENEMY_SPRITES

MINION_ATTRIBUTES = {
    'name':  "minion",
    'health': 15,
    'speed' : 1,
    'damage': 2
}

RUNNER_ATTRIBUTES = {
    'name':  "runner",
    'health': 12,
    'speed' : 2,
    'damage': 1
}

FATMAN_ATTRIBUTES = {
    'name':  "fatman",
    'health': 48,
    'speed' : 0.5,
    'damage': 4
}

class _Mob(pg.sprite.Sprite):
    def __init__(self, image_path, cors, path):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_path, -1)
        self.position = pg.Vector2(cors)
        self.rect.center = self.position
        self.path = path
        self._next_block_index = 0
        self.done = False

    def update_attributes(self):
        pass

    def update(self):
        reached_destiny = self._next_block_index == len(self.path)
        if not reached_destiny:
            position_target = pg.Vector2(self.path[self._next_block_index])

            if self.position == position_target:
                if self._next_block_index < len(self.path) - 1:
                    self._next_block_index += 1
                else: self.done = True
            else:
                self.position += (position_target - self.position).normalize() * self.speed
                self.rect.center = self.position

    def draw(self, surface):
        if not self.done: surface.blit(self.image, self.rect.topleft)

class Minion(_Mob):
    def __init__(self, level, cors, path):
        super().__init__(ENEMY_SPRITES["minion"], cors, path)
        self.__dict__.update(MINION_ATTRIBUTES)
        self.reward = randint(21, 26)
        self.level = level
        if level > 1: self.update_attributes()

    def update_attributes(self):
        self.health += (self.level - 1) * 0.5
        self.speed += (self.level - 1) * 0.2
        self.damage += (self.level - 1) * 1

    def update(self):
        super().update()

    def draw(self, surface):
        super().draw(surface)

class Runner(_Mob):
    def __init__(self, level, cors, path):
        super().__init__(ENEMY_SPRITES["runner"], cors, path)
        self.__dict__.update(RUNNER_ATTRIBUTES)
        self.reward = randint(10, 15)
        self.level = level
        if level > 1: self.update_attributes()

    def update_attributes(self):
        self.health += (self.level - 1) * 0.2
        self.speed += (self.level - 1) * 0.2
        self.damage += (self.level - 1) * 0.2

    def update(self):
        super().update()

class Fatman(_Mob):
    def __init__(self, level, cors, path):
        super().__init__(ENEMY_SPRITES["fatman"], cors, path)
        self.__dict__.update(FATMAN_ATTRIBUTES)
        self.reward = randint(44, 56)
        self.level = level
        if level > 1: self.update_attributes()

    def update_attributes(self):
        self.health += (self.level - 1) * 1.5
        self.speed += (self.level - 1) * 0.4
        self.damage += (self.level - 1) * 0.4

    def update(self):
        super().update()
