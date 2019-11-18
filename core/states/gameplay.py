import pygame as pg

from .. import state_machine
from ..components import mobs
from ..components import towers
from ..utils import COLORS, HEIGHT, MODE, TITLE, WIDTH, BEGIN_SPRITE, END_SPRITE, load_image
from ..bullet import Bullet


class Gameplay(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        self.new_bullets = []

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)
        self.all_sprites = pg.sprite.Group()

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
        begin.image, begin.rect = load_image(BEGIN_SPRITE, -1)
        begin.image = pg.transform.scale(begin.image, (100,100))
        begin.rect.center = full_path[0]
        self.all_sprites.add(begin)

        for i in range(8):
            path = pg.sprite.Sprite()
            path.image = pg.Surface((100, 100))
            path.image.fill(COLORS['path'])
            path.rect = path.image.get_rect()
            path.rect.center = full_path[i+1]
            self.all_sprites.add(path)

        end = pg.sprite.Sprite()
        end.image, end.rect = load_image(END_SPRITE, -1)
        end.image = pg.transform.scale(end.image, (100,100))
        end.rect.center = full_path[-1]
        self.all_sprites.add(end)

        base = pg.sprite.Sprite()
        base.image = pg.Surface((100, 100))
        base.image.fill(COLORS['base'])
        base.rect = base.image.get_rect()
        base.rect.center = (WIDTH / 2, 700)
        self.all_sprites.add(base)

        minion = mobs.Minion(full_path[0], full_path)
        self.all_sprites.add(minion)

        mob_list = [minion]

        turret = towers.Turret((WIDTH / 2, 300), mob_list, self.new_bullets)
        self.all_sprites.add(turret)

    def get_event(self, event):
        pass

    def update(self, keys, now):
        self.all_sprites.update()
        for bullet in self.new_bullets:
            cors = bullet[0]
            mob = bullet[1]
            speed = bullet[2]
            new_bullet = Bullet(cors, mob, speed)
            self.all_sprites.add(new_bullet)
            self.new_bullets.pop()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.all_sprites.draw(surface)
