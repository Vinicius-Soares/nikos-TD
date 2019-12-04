# Torres do jogo
import enum
import math
import pygame as pg
import random

from .bullets import TurretBullet
from ..constants import TOWER_SPRITES
from ..controllers import sound_controller as sc
from ..tools import load_image


TURRET_ATTRIBUTES = {
    'name':        "turret",
    'damage':       2,
    'fire_range':   125,
    'fire_rate':    1.6,
    'bullet_speed': 6,
    'cost': 100
}


BOMBER_ATTRIBUTES = {
    'name':       "bomber",
    'damage':      6,
    'fire_range':  250,
    'fire_rate':   50,
    'fire_radius': 50,
    'cost': 150
}


SNIPER_ATTRIBUTES = {
    'name':         "sniper",
    'damage':       15,
    'fire_range':   500,
    'fire_rate':    1.2,
    'bullet_speed': 18,
    'cost':         350
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
        self.can_shoot = False
        self.done = False
        self.last_bullet_time = pg.time.get_ticks()
        self.behavior = TowerBehavior.RANDOM

    def is_in_range(self, obj):
        return self.position.distance_to(obj.position) < self.fire_range

    def search_target(self, mobs):
        if self.behavior == TowerBehavior.FIRST:
            self.target = mobs[0]
        elif self.behavior == TowerBehavior.RANDOM:
            mobs_length = len(mobs)
            random_index = random.randint(0, mobs_length - 1)
            self.target = mobs[random_index]
        elif self.behavior == TowerBehavior.STRONG:
            stronger = mobs[0]
            health = mobs[0].health
            for mob in mobs[1:]:
                if mob.health > health:
                    health = mob.health
                    stronger = mob
            self.target = stronger
        else:
            weaker = mobs[0]
            health = mobs[0].health
            for mob in mobs[1:]:
                if mob.health < health:
                    health = mob.health
                    weaker = mob
            self.target = weaker

    def fire(self):
        pass

    def update(self, now, mobs):
        if not self.target:
            mobs_in_range = [mob for mob in mobs if self.is_in_range(mob)]
            if len(mobs_in_range) > 0: self.search_target(mobs_in_range)
        else:
            if now - self.last_bullet_time >= (1 / self.fire_rate) * 1000:
                self.can_shoot = True
                self.last_bullet_time = now

            if self.target.done or \
                not self.is_in_range(self.target): self.target = None

        for bullet in self.bullets:
            if not self.is_in_range(bullet): bullet.done = True

            if not bullet.done: bullet.update()
            else: self.bullets.remove(bullet)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        for bullet in self.bullets:
            bullet.draw(surface)


class Turret(_Tower):
    def __init__(self, cors):
        super().__init__(TOWER_SPRITES["turret"], cors)
        self.__dict__.update(TURRET_ATTRIBUTES)

    def update(self, now, mobs):
        super().update(now, mobs)
        if self.can_shoot: self.fire()

    def fire(self):
        new_bullet = TurretBullet(self.position, self.name, self.target, self.damage, self.bullet_speed)
        self.bullets.append(new_bullet)
        sc.SoundController().play_turret_shot()
        self.can_shoot = False


class Bomber(_Tower):
    def __init__(self, cors):
        super().__init__(TOWER_SPRITES["bomber"], cors)
        self.__dict__.update(BOMBER_ATTRIBUTES)

    def update(self, now, mobs):
        super().update(now, mobs)

    def fire(self):
        pass


class Sniper(_Tower):
    def __init__(self, cors):
        super().__init__(TOWER_SPRITES["sniper"], cors)
        self.__dict__.update(SNIPER_ATTRIBUTES)

    def update(self, now, mobs):
        super().update(now, mobs)

    def fire(self):
        pass
