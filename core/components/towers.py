# Torres do jogo
import enum
import math
import pygame as pg

from .bullet import Bullet
from ..tools import load_image
from ..constants import TOWER_SPRITES

TURRET_ATTRIBUTES = {
    'name':       "turret",
    'damage':      1,
    'fire_range':  300,
    'fire_rate':   0.6,
    'bullet_speed': 0.8
}

BOMBER_ATTRIBUTES = {
    'name':       "bomber",
    'damage':      5,
    'fire_range':  250,
    'fire_rate':   50,
    'fire_radius': 10
}

SNIPER_ATTRIBUTES = {
    'name':      "sniper",
    'damage':     1,
    'fire_range': 500,
    'fire_rate':  75,
    'bullet_speed': 1.3
}


class TowerBehavior(enum.Enum):
    RANDOM = 1
    FIRST = 2
    STRONG = 3
    WEAK = 4

class _Tower(pg.sprite.Sprite):
    def __init__(self, image_path, cors):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_path, -1)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.position = pg.Vector2(cors)
        self.rect.center = self.position
        self.bullets = []
        self.target = None
        self.done = False
        self.last_bullet_time = pg.time.get_ticks()
        self.behavior = TowerBehavior.FIRST

    def update(self, now, mobs):
        self.search_target(mobs)
        if self.target and \
            now - self.last_bullet_time >= (1 / self.fire_rate) * 1000:
            self.fire()
            self.last_bullet_time = now

        for bullet in self.bullets:
            if not bullet.done: bullet.update()
            else:
                self.bullets.remove(bullet)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        for bullet in self.bullets:
            bullet.draw(surface)

    def search_target(self, mobs):
        if self.behavior == TowerBehavior.RANDOM: pass
        elif self.behavior == TowerBehavior.FIRST:
            for mob in mobs:
                if self.is_in_range(mob):
                    self.target = mob
                    break
        elif self.behavior == TowerBehavior.STRONG: pass
        else: pass

    def fire(self):
        new_bullet = Bullet(self.position, self.target, self.bullet_speed)
        self.bullets.append(new_bullet)

    def is_in_range(self, mob):
        return self.position.distance_to(mob.position) < self.fire_range

class Turret(_Tower):
    def __init__(self, cors):
        super().__init__(TOWER_SPRITES["turret"], cors)
        self.__dict__.update(TURRET_ATTRIBUTES)

    def update(self, now, mobs):
        super().update(now, mobs)

    def draw(self, surface):
        super().draw(surface)


class Bomber(_Tower):
    def __init__(self, cors):
        super().__init__(TOWER_SPRITES["bomber"], cors)
        self.__dict__.update(BOMBER_ATTRIBUTES)

    def update(self):
        pass

    def fire(self):
        pass


class Sniper(_Tower):
    def __init__(self, cors):
        super().__init__(TOWER_SPRITES["sniper"], cors)
        self.__dict__.update(SNIPER_ATTRIBUTES)

    def update(self):
        pass

    def fire(self):
        pass
