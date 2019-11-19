# Torres do jogo
import pygame as pg
from enum import Enum

from .bullet import Bullet
from ..utils import load_image, TURRET_SPRITE, BOMBER_SPRITE, SNIPER_SPRITE

class TowerBehavior(Enum):
    FIRST = 1
    RANDOM = 2
    STRONG = 3
    WEAK = 4

class _Tower(pg.sprite.Sprite):
    def __init__(self, image_path, damage, fire_range, fire_rate, cors, mobs, bullets):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_path, -1)
        self.image = pg.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.damage = damage
        self.fire_range = fire_range
        self.fire_rate = fire_rate
        self.x_cor, self.y_cor = cors
        self.rect.center = cors
        self.bullets = bullets
        self.mobs = mobs
        self.timer = 200
        self.behavior = TowerBehavior.FIRST

    def update(self):
        if self.timer == 200:
            self.timer = 0
            for mob in self.mobs:
                is_in_range = (self.x_cor-mob.x_cor)**2 + (self.y_cor-mob.y_cor)**2 < self.fire_range**2
                if is_in_range:
                    new_bullet = Bullet((self.x_cor, self.y_cor), mob, 2)
                    self.bullets.add(new_bullet)
        self.timer += 1

    def fire(self):
        pass

class Turret(_Tower):
    def __init__(self, cors, mobs, bullets):
        super().__init__(TURRET_SPRITE, 1,300, 200, cors, mobs, bullets)

    def update(self):
        super().update()
        
    
    def fire(self):
        pass

class Bomber(_Tower):
    def __init__(self, cors, mobs):
        super().__init__(BOMBER_SPRITE, 1,1,1, cors)

    def update(self):
        pass

    def fire(self):
        pass

class Sniper(_Tower):
    def __init__(self, cors, mobs):
        super().__init__(SNIPER_SPRITE, 1,1,1, cors)

    def update(self):
        pass

    def fire(self):
        pass
    