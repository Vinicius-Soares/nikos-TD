import pygame as pg
from ..utils import load_image, BULLET_SPRITE

class Bullet(pg.sprite.Sprite):
    def __init__(self, cors, target, speed):
        super().__init__()
        self.image = pg.transform.scale(load_image(BULLET_SPRITE, -1)[0], (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = cors
        self.origin = cors
        self.x_cor, self.y_cor = cors
        self.target = target
        self.speed= speed
        self.damage = 2

    def update(self):
        self._dx = ((self.target.x_cor-self.x_cor)*self.speed)/10
        self._dy = ((self.target.y_cor-self.y_cor)*self.speed)/10

        self.x_cor += self._dx
        self.y_cor += self._dy

        self.rect.center = (self.x_cor, self.y_cor)
        hit_target = self.rect.colliderect(self.target.rect)
        if hit_target:
            self.target.health -= self.damage
            if self.target.health <= 0: self.target.kill()
            self.kill()
