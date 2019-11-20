import pygame as pg

from .. import state_machine
from ..components import mobs
from ..components import towers
from ..utils import COLORS, HEIGHT, MODE, TITLE, WIDTH, PATH_TYPES, TOWERPLACE_SPRITE, load_image


class Gameplay(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        self.all_sprites = pg.sprite.Group()
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
        self.money = 100
        print(self.money)

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)

        self.tower_places = []
        self.mobs = []
        self.bullets = []

        begin = EnemyPath("begin", self.full_path[0])
        self.all_sprites.add(begin)

        for i in range(7):
            path = EnemyPath("enemy", self.full_path[i+1])
            self.all_sprites.add(path)

        end = EnemyPath("end", self.full_path[-1])
        self.all_sprites.add(end)

        base = TowerPlace((WIDTH / 2, 300))
        self.tower_places.append(base)

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            x, y = pg.mouse.get_pos()
            for tower_place in self.tower_places:
                if tower_place.click_on_it(x, y):
                    print("Click!")
                    tower_place.set_tower("turret", self.mobs, self.bullets)

    def update(self, keys, now):
        if(self.i % 150 == 0):
            minion = mobs.Minion(1, self.full_path[0], self.full_path)
            self.mobs.append(minion)

        self.all_sprites.update()

        for tower_place in self.tower_places:
            tower_place.update()

        for bullet in self.bullets:
            if not bullet.done: bullet.update()
            else:
                self.bullets.remove(bullet)

        for mob in self.mobs:
            if not mob.done: mob.update()
            else:
                if mob.health <= 0:
                    self.money += mob.reward
                    print(self.money)
                self.mobs.remove(mob)

        self.i += 1

    def draw(self, surface):
        surface.fill((0, 0, 0))

        self.all_sprites.draw(surface)

        for tower_place in self.tower_places:
            tower_place.draw(surface)

        for bullet in self.bullets:
            bullet.draw(surface)

        for mob in self.mobs:
            mob.draw(surface)


class EnemyPath(pg.sprite.Sprite):
    def __init__(self, path_type, cors):
        super().__init__()
        self.type = path_type
        self.image = pg.transform.scale(load_image(PATH_TYPES[path_type], -1)[0], (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = cors
    


class TowerPlace(pg.sprite.Sprite):
    def __init__(self, cors):
        super().__init__()
        self.image = pg.transform.scale(load_image(TOWERPLACE_SPRITE, -1)[0], (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = cors
        self.tower = None
        self.selected = False

    def set_tower(self, tower_name, mobs, bullets):
        if tower_name == "turret":
            tower_rect_center = (self.rect.center[0] + 25, self.rect.center[1] + 25)
            self.tower = towers.Turret(tower_rect_center, mobs, bullets)

    def remove_tower(self):
        self.tower = None

    def click_on_it(self, x, y):
        return self.rect.collidepoint(x, y)

    def update(self):
        if self.tower: self.tower.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect.center)
        if self.tower: self.tower.draw(surface)
        if self.selected: pass
