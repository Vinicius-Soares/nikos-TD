import pygame as pg

from . import towers
from ..tools import load_image
from ..constants import PATH_TYPES, TOWERPLACE_SPRITE

class EnemyPath(pg.sprite.Sprite):
    def __init__(self, path_type, cors):
        super().__init__()
        self.type = path_type
        self.image = pg.transform.scale(load_image(PATH_TYPES[path_type], -1)[0], (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = cors


class TowerPlace(pg.sprite.Sprite):
    def __init__(self, cors):
        super().__init__()
        self.image = pg.transform.scale(load_image(TOWERPLACE_SPRITE, -1)[0], (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = cors
        self.tower = None
        self.selected = False

    def set_tower(self, tower_name):
        if tower_name == "turret":
            self.tower = towers.Turret(self.rect.center)
        elif tower_name == "bomber": pass
        else: pass

    def remove_tower(self):
        self.tower = None

    def click_on_it(self, x, y):
        return self.rect.collidepoint(x, y)

    def update(self, now, mobs):
        if self.tower: self.tower.update(now, mobs)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if self.tower: self.tower.draw(surface)
        if self.selected: pass
