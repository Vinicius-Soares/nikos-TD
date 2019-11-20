import pygame as pg
from ..tools import load_image
from ..constants import BULLET_SPRITES

class Bullet(pg.sprite.Sprite):
    def __init__(self, cors, target, speed):
        super().__init__()
        self.image = pg.transform.scale(load_image(BULLET_SPRITES["turret"], -1)[0], (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = cors
        self.origin = cors
        self.x_cor, self.y_cor = cors
        self.target = target
        self.speed= speed
        self.damage = 2
        self.done = False

    def update(self):
        self._dx = ((self.target.x_cor-self.x_cor) * self.speed) / 10
        self._dy = ((self.target.y_cor-self.y_cor) * self.speed) / 10

        self.x_cor += self._dx
        self.y_cor += self._dy

        self.rect.center = (self.x_cor, self.y_cor)
        hit_target = self.rect.colliderect(self.target.rect)
        if hit_target:
            self.target.health -= self.damage
            if self.target.health <= 0: self.target.done = True
            self.done = True

    def draw(self, surface):
        if not self.done: surface.blit(self.image, self.rect.center)
