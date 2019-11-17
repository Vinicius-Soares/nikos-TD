import pygame as pg

from .. import state_machine
from ..towers import Turret
from ..mobs import Minion
from ..utils import COLORS, HEIGHT, MODE, TITLE, WIDTH, load_image, BEGIN_SPRITE


class Gameplay(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)
        self.all_sprites = pg.sprite.Group()

        begin = pg.sprite.Sprite()
        begin.image = pg.Surface((100, 100))
        begin.image.fill(COLORS['begin'])
        begin.rect = begin.image.get_rect()
        begin.rect.center = (100, HEIGHT / 2)
        self.all_sprites.add(begin)

        for i in range(8):
            path = pg.sprite.Sprite()
            path.image = pg.Surface((100, 100))
            path.image.fill(COLORS['path'])
            path.rect = path.image.get_rect()
            path.rect.center = (190 + (i * 100), HEIGHT / 2)
            self.all_sprites.add(path)

        end = pg.sprite.Sprite()
        end.image = pg.Surface((100, 100))
        end.image.fill(COLORS['end'])
        end.rect = end.image.get_rect()
        end.rect.center = (900, HEIGHT / 2)
        self.all_sprites.add(end)

        base = pg.sprite.Sprite()
        base.image = pg.Surface((100, 100))
        base.image.fill(COLORS['base'])
        base.rect = base.image.get_rect()
        base.rect.center = (WIDTH / 2, 500)
        self.all_sprites.add(base)

        turret = Turret(WIDTH / 2, 500)
        self.all_sprites.add(turret)

        minion = Minion(100, 100)
        self.all_sprites.add(minion)

    def get_event(self, event):
        pass

    def update(self, keys, now):
        pass

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.all_sprites.draw(surface)
