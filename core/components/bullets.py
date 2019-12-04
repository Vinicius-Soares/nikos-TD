import pygame as pg
from math import atan2, degrees, cos, sin, pi

from ..tools import load_image
from ..constants import BULLET_SPRITES
from ..controllers import sound_controller as sc

class Bullet(pg.sprite.Sprite):
    def __init__(self, position, type, target, damage, speed):
        super().__init__()
        self.type = type
        if self.type == "bomber":
            scale = (56, 56)
        else:
            scale = (7, 7)
        self.image = pg.transform.scale(load_image(BULLET_SPRITES[self.type], -1)[0], scale)
        self.rect = self.image.get_rect()
        self.position = pg.Vector2(position)
        self.rect.center = position
        self.target = target
        self.damage = damage
        self.speed = speed
        self.done = False

    def update(self):
        if not self.target: return
        self.position += (self.target.position - self.position).normalize() * self.speed
        self.rect.center = self.position

        hit_target = self.rect.colliderect(self.target.rect)
        
        if hit_target:
            self.target.health -= self.damage

            if self.target.health <= 0: 
                self.target.done = True
                sc.SoundController().play_mob_death()
            
            self.done = True

    def draw(self, surface):
        if not self.done: surface.blit(self.image, self.rect.topleft)
