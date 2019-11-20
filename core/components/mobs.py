# Inimigos do jogo
import pygame as pg
from ..utils import load_image, MINION_SPRITE, RUNNER_SPRITE, FATMAN_SPRITE

MINION_ATTRIBUTES = {
    'name':  "minion",
    'health': 4,
    'speed' : 1,
    'damage': 1,
    'reward': 24
}

RUNNER_ATTRIBUTES = {
    'name':  "runner",
    'health': 2,
    'speed' : 1.5,
    'damage': 0.5,
    'reward': 12
}

FATMAN_ATTRIBUTES = {
    'name':  "fatman",
    'health': 8,
    'speed' : 0.3,
    'damage': 2,
    'reward': 50
}

class _Mob(pg.sprite.Sprite):
    def __init__(self, image_path, cors, path):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_path, -1)
        self.x_cor, self.y_cor = cors
        self.rect.center = cors
        self.path = path
        self._next_block_index = 0
        self.done = False

    def update_attributes(self):
        pass

    def update(self):
        reached_destiny = self._next_block_index == len(self.path)
        if not reached_destiny:
            next_x, next_y = self.path[self._next_block_index]

            if self.x_cor == next_x and self.y_cor == next_y:
                if self._next_block_index < len(self.path) - 1:
                    self._next_block_index += 1
                else: self.done = True
                block_x, block_y = self.path[self._next_block_index]

                current_block_index = self._next_block_index - 1
                current_block_x, current_block_y = self.path[current_block_index]

                self._dx = (block_x - current_block_x) / (100-self.speed)
                self._dy = (block_y - current_block_y) / (100-self.speed)

            else:
                self.x_cor += int(self._dx)
                self.y_cor += int(self._dy)
                self.rect.center = (self.x_cor, self.y_cor)

    def draw(self, surface):
        if not self.done: surface.blit(self.image, self.rect.center)

class Minion(_Mob):
    def __init__(self, level, cors, path):
        super().__init__(MINION_SPRITE, cors, path)
        self.__dict__.update(MINION_ATTRIBUTES)
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
        super().__init__(RUNNER_SPRITE, cors, path)
        self.__dict__.update(RUNNER_ATTRIBUTES)
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
        super().__init__(FATMAN_SPRITE, cors, path)
        self.__dict__.update(FATMAN_ATTRIBUTES)
        self.level = level
        if level > 1: self.update_attributes()

    def update_attributes(self):
        self.health += (self.level - 1) * 1.5
        self.speed += (self.level - 1) * 0.4
        self.damage += (self.level - 1) * 0.4

    def update(self):
        super().update()
