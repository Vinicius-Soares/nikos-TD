import pygame as pg
from .utils import load_image, BULLET_SPRITE

class Bullet(pg.sprite.Sprite):
    def __init__(self, cors, target, speed):
        super().__init__()
        self.image, self.rect = load_image(BULLET_SPRITE, -1)
        self.origin = cors
        self.x_cor, self.y_cor = cors
        self.target = target
        self.speed= speed

    def update(self):
        self._dx = ((self.target.x_cor-self.x_cor)*self.speed)/200
        self._dy = ((self.target.y_cor-self.y_cor)*self.speed)/200

        self.x_cor+=self._dx
        self.y_cor+=self._dy

        self.rect.center = (self.x_cor, self.y_cor)
        hit_target = self.rect.colliderect(self.target.rect)
        if hit_target: self.kill()