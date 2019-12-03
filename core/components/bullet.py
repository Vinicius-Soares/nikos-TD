import pygame as pg
from math import atan2, degrees, cos, sin, pi
from ..tools import load_image
from ..constants import BULLET_SPRITES, SOUNDS

class Bullet(pg.sprite.Sprite):
    def __init__(self, position, target, damage, speed):
        super().__init__()
        self.image = pg.transform.scale(load_image(BULLET_SPRITES["turret"], -1)[0], (7, 7))
        self.rect = self.image.get_rect()
        self.position = pg.Vector2(position)
        self.rect.center = position
        self.target = target
        self.damage = damage
        self.speed = speed
        self.done = False
        self.mob_death_sound = pg.mixer.Sound(SOUNDS["mob_death"].as_posix())

    def update(self):
        self.position += (self.target.position - self.position).normalize() * self.speed
        self.rect.center = self.position

        hit_target = self.rect.colliderect(self.target.rect)
        
        if hit_target:
            self.target.health -= self.damage
            if self.target.health <= 0: 
                self.target.done = True
                self.mob_death_sound.play()
            self.done = True

    def draw(self, surface):
        if not self.done: surface.blit(self.image, self.rect.topleft)
