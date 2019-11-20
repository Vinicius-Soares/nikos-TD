# Torres do jogo
import pygame as pg
from .bullet import Bullet
from ..utils import load_image, TURRET_SPRITE, BOMBER_SPRITE, SNIPER_SPRITE

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
        self.target = None
        self.timer = 100

    def update(self):
        if self.timer == 100:
            print(self.target)
            self.timer = 0
            if self.target:
                if not self.is_in_range(self.target) or self.target.health<=0:
                    self.target = None
            mob_index = 0
            while mob_index < len(self.mobs) and self.target is None:
                if self.is_in_range(self.mobs.sprites()[mob_index]): 
                    self.target = self.mobs.sprites()[mob_index]
                mob_index+=1
            if self.target:
                self.fire(self.target)
        self.timer+= 1

    def fire(self, mob):
        new_bullet = Bullet((self.x_cor, self.y_cor), mob, 2)
        self.bullets.add(new_bullet)

    def is_in_range(self, mob):
        x, xo, y, yo = self.x_cor, mob.x_cor, self.y_cor, mob.y_cor
        return (x-xo)**2 + (y-yo)**2 < self.fire_range**2


class Turret(_Tower):
    def __init__(self, cors, mobs, bullets):
        super().__init__(TURRET_SPRITE, 1,300, 100, cors, mobs, bullets)

    def update(self):
        super().update()
    

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
    