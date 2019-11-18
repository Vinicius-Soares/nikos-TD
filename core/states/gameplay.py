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

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)

        full_path = ((100, 100),
                     (100, 200),
                     (200, 200),
                     (200, 300),
                     (300, 300),
                     (300, 400),
                     (400, 400),
                     (400, 500),
                     (500, 500))

        full_path = full_path[::-1]

        begin = pg.sprite.Sprite()
        begin.image = pg.transform.scale(load_image(BEGIN_SPRITE, -1)[0], (100,100))
        begin.rect = begin.image.get_rect()
        begin.rect.center = full_path[0]
        self.all_sprites.add(begin)

        for i in range(7):
            path = pg.sprite.Sprite()
            path.image = pg.transform.scale(load_image(ENEMYPATH_SPRITE, -1)[0], (100,100))
            path.rect = path.image.get_rect()
            path.rect.center = full_path[i+1]
            self.all_sprites.add(path)

        end = pg.sprite.Sprite()
        end.image = pg.transform.scale(load_image(END_SPRITE, -1)[0], (100,100))
        end.rect = end.image.get_rect()
        end.rect.center = full_path[-1]
        self.all_sprites.add(end)

        base = pg.sprite.Sprite()
        base.image = pg.transform.scale(load_image(TOWERPLACE_SPRITE, -1)[0], (100,100))
        base.rect = base.image.get_rect()
        base.rect.center = (WIDTH / 2, 300)
        self.all_sprites.add(base)

        minion = mobs.Minion(full_path[0], full_path)
        self.all_sprites.add(minion)

        mob_list = [minion]

        turret = towers.Turret((WIDTH / 2, 300), mob_list, self.bullets)
        self.all_sprites.add(turret)

    def get_event(self, event):
        pass

    def update(self, keys, now):
        self.all_sprites.update()
        self.bullets.update()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.all_sprites.draw(surface)
        self.bullets.draw(surface)
