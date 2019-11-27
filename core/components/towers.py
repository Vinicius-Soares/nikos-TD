# Torres do jogo
import pygame as pg
from .bullet import Bullet
from ..tools import load_image
from ..constants import TOWER_SPRITES

TURRET_ATTRIBUTES = {
    'name':       "turret",
    'damage':      1,
    'fire_range':  300,
    'fire_rate':   100
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
    'fire_rate':  75
}


class _Tower(pg.sprite.Sprite):
    def __init__(self, image_path, cors, mobs):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(image_path, -1)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.x_cor, self.y_cor = cors
        self.rect.center = cors
        self.bullets = []
        self.mobs = mobs
        self.target = None
        self.timer = 100
        self.done = False

    def update(self):
        if self.timer == 100:
            self.timer = 0
            if self.target:
                if not self.is_in_range(self.target) or self.target.health <= 0:
                    self.target = None
            mob_index = 0
            while mob_index < len(self.mobs) and self.target is None:
                if self.is_in_range(self.mobs[mob_index]):
                    self.target = self.mobs[mob_index]
                mob_index += 1
            if self.target:
                self.fire()
        self.timer += 1

        for bullet in self.bullets:
            if not bullet.done: bullet.update()
            else:
                self.bullets.remove(bullet)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        for bullet in self.bullets:
            bullet.draw(surface)

    def search_target(self):
        pass

    def fire(self):
        new_bullet = Bullet((self.x_cor, self.y_cor), self.target, 2)
        self.bullets.append(new_bullet)

    def is_in_range(self, mob):
        x, xo, y, yo = self.x_cor, mob.x_cor, self.y_cor, mob.y_cor
        return (x-xo)**2 + (y-yo)**2 < self.fire_range**2


class Turret(_Tower):
    def __init__(self, cors, mobs):
        super().__init__(TOWER_SPRITES["turret"], cors, mobs)
        self.__dict__.update(TURRET_ATTRIBUTES)

    def update(self):
        super().update()

    def draw(self, surface):
        super().draw(surface)


class Bomber(_Tower):
    def __init__(self, cors, mobs):
        super().__init__(TOWER_SPRITES["bomber"], cors, [], [])
        self.__dict__.update(BOMBER_ATTRIBUTES)

    def update(self):
        pass

    def fire(self):
        pass


class Sniper(_Tower):
    def __init__(self, cors, mobs):
        super().__init__(TOWER_SPRITES["sniper"], cors, [], [])
        self.__dict__.update(SNIPER_ATTRIBUTES)

    def update(self):
        pass

    def fire(self):
        pass
