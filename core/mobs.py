# Inimigos do jogo
import pygame as pg
from .utils import load_image, MINION_SPRITE, RUNNER_SPRITE, FATMAN_SPRITE

class _Mob(pg.sprite.Sprite):
    def __init__(self, image_path, damage, speed, attack_rate, angle, x_cor, y_cor):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_path, -1)
        self.damage = damage
        self.speed = speed
        self.attack_rate = attack_rate
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.angle = angle
        self.rect.center = (x_cor, y_cor)

    def update(self):
        pass
    
    def fire(self):
        pass

class Minion(_Mob):
    def __init__(self, x_cor, y_cor):
        super().__init__(MINION_SPRITE, 1,1,1, x_cor, y_cor)

    def update(self):
        pass
    
    def fire(self):
        pass

class Runner(_Mob):
    def __init__(self, x_cor, y_cor):
        super().__init__(RUNNER_SPRITE, 1,1,1, x_cor, y_cor)

    def update(self):
        pass

    def fire(self):
        pass

class Fatman(_Mob):
    def __init__(self, x_cor, y_cor):
        super().__init__(FATMAN_SPRITE, 1,1,1, x_cor, y_cor)

    def update(self):
        pass

    def fire(self):
        pass