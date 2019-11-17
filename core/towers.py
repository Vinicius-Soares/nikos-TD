# Torres do jogo
import pygame as pg
from .utils import load_image, TURRET_SPRITE, BOMBER_SPRITE, SNIPER_SPRITE

class _Tower(pg.sprite.Sprite):
    def __init__(self, image_path, damage, fire_range, fire_rate, x_cor, y_cor):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_path, -1)
        self.damage = damage
        self.fire_range = fire_range
        self.fire_rate = fire_rate
        self.x_cor = x_cor
        self.y_cor = y_cor
        # self.angle = angle
        self.rect.center = (x_cor, y_cor)

    def update(self):
        pass
    
    def fire(self):
        pass

class Turret(_Tower):
    def __init__(self, x_cor, y_cor):
        super().__init__(TURRET_SPRITE, 1,3,1, x_cor, y_cor)

    def update(self):
        pass
    
    def fire(self):
        pass

class Bomber(_Tower):
    def __init__(self, x_cor, y_cor):
        super().__init__(BOMBER_SPRITE, 1,1,1, x_cor, y_cor)

    def update(self):
        pass

    def fire(self):
        pass

class Sniper(_Tower):
    def __init__(self, x_cor, y_cor):
        super().__init__(SNIPER_SPRITE, 1,1,1, x_cor, y_cor)

    def update(self):
        pass

    def fire(self):
        pass