import pygame as pg

from .. import state_machine
from ..components import mobs
from ..components import towers
from ..utils import COLORS, HEIGHT, MODE, TITLE, WIDTH, BEGIN_SPRITE, END_SPRITE, ENEMYPATH_SPRITE, TOWERPLACE_SPRITE, load_image


class Gameplay(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        self.bullets = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.full_path = ((100, 100),
                          (100, 200),
                          (200, 200),
                          (200, 300),
                          (300, 300),
                          (300, 400),
                          (400, 400),
                          (400, 500),
                          (500, 500))[::-1]
        self.i = 0

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)

        begin = pg.sprite.Sprite()
        begin.image = pg.transform.scale(load_image(BEGIN_SPRITE, -1)[0], (100,100))
        begin.rect = begin.image.get_rect()
        begin.rect.center = self.full_path[0]
        self.all_sprites.add(begin)

        for i in range(7):
            path = pg.sprite.Sprite()
            path.image = pg.transform.scale(load_image(ENEMYPATH_SPRITE, -1)[0], (100,100))
            path.rect = path.image.get_rect()
            path.rect.center = self.full_path[i+1]
            self.all_sprites.add(path)

        end = pg.sprite.Sprite()
        end.image = pg.transform.scale(load_image(END_SPRITE, -1)[0], (100,100))
        end.rect = end.image.get_rect()
        end.rect.center = self.full_path[-1]
        self.all_sprites.add(end)

        base = pg.sprite.Sprite()
        base.image = pg.transform.scale(load_image(TOWERPLACE_SPRITE, -1)[0], (100,100))
        base.rect = base.image.get_rect()
        base.rect.center = (WIDTH / 2, 300)
        self.all_sprites.add(base)

        turret = towers.Turret((WIDTH / 2, 300), self.mobs, self.bullets)
        self.all_sprites.add(turret)

    def get_event(self, event):
        pass

    def update(self, keys, now):
        if(self.i % 150 == 0):
            minion = mobs.Minion(1, self.full_path[0], self.full_path)
            self.mobs.add(minion)
        self.all_sprites.update()
        self.mobs.update()
        self.bullets.update()
        self.i += 1

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.all_sprites.draw(surface)
        self.mobs.draw(surface)
        self.bullets.draw(surface)
