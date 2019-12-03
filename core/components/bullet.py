import pygame as pg
from math import atan2, degrees, cos, sin, pi
from ..tools import load_image
from ..constants import BULLET_SPRITES

class Bullet(pg.sprite.Sprite):
    def __init__(self, cors, target, speed):
        super().__init__()
        self.image = pg.transform.scale(load_image(BULLET_SPRITES["turret"], -1)[0], (7, 7))
        self.rect = self.image.get_rect()
        self.rect.center = cors
        self.origin = cors
        self.position = pg.Vector2(cors)
        self.target = target
        self.speed= speed
        self.damage = 2
        self.done = False

    def update(self):
        position_target = pg.Vector2(self.target.x_cor, self.target.y_cor)

        self.position += (position_target - self.position).normalize() * 4

        self.rect.center = self.position
        hit_target = self.rect.colliderect(self.target.rect)
        if hit_target:
            self.target.health -= self.damage
            if self.target.health <= 0: self.target.done = True
            self.done = True

    def draw(self, surface):
        if not self.done: surface.blit(self.image, self.rect.topleft)
