# Inimigos do jogo
import pygame as pg
from ..utils import load_image, MINION_SPRITE, RUNNER_SPRITE, FATMAN_SPRITE

class _Mob(pg.sprite.Sprite):
    def __init__(self, image_path, damage, speed, attack_rate, cors, path):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_path, -1)
        self.damage = damage
        self.speed = speed
        self.attack_rate = attack_rate
        self.x_cor, self.y_cor = cors
        self.path = path
        self.rect.center = cors
        self._next_block_index = 0

    def update(self):
        reached_destiny = self._next_block_index == len(self.path)

        if not reached_destiny:
            next_x, next_y = self.path[self._next_block_index]

            if self.x_cor == next_x and self.y_cor == next_y:
                if self._next_block_index < len(self.path) - 1:
                    self._next_block_index+=1
                block_x, block_y = self.path[self._next_block_index]

                current_block_index = self._next_block_index-1
                current_block_x, current_block_y = self.path[current_block_index]

                self._dx = (block_x - current_block_x)/(100-self.speed)
                self._dy = (block_y - current_block_y)/(100-self.speed)

            else:
                self.x_cor+=int(self._dx)
                self.y_cor+=int(self._dy)
                self.rect.center = (self.x_cor, self.y_cor)
    
    
    def fire(self):
        pass

class Minion(_Mob):
    def __init__(self, cors, path):
        self._next_block_index = 0
        super().__init__(MINION_SPRITE, 1,1,1, cors, path)

    def update(self):
        super().update()
    
    def fire(self):
        pass

class Runner(_Mob):
    def __init__(self, cors):
        x_cor, y_cor = cors
        super().__init__(RUNNER_SPRITE, 1,1,1, x_cor, y_cor)

    def update(self):
        super().update()

    def fire(self):
        pass

class Fatman(_Mob):
    def __init__(self, cors):
        x_cor, y_cor = cors
        super().__init__(FATMAN_SPRITE, 1,1,1, x_cor, y_cor)

    def update(self):
        super().update()
        
    def fire(self):
        pass
    