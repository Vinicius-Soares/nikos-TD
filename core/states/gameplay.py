import pygame as pg

from .. import state_machine
from ..components import map_components, mobs
from ..tools import load_image
from ..constants import PATH_TYPES, TOWERPLACE_SPRITE

class Gameplay(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        self.all_sprites = pg.sprite.Group()
        self.full_path = ((96, 96),
                          (96, 160),
                          (96, 224),
                          (160, 224),
                          (224, 224),
                          (288, 224),
                          (352, 224),
                          (416, 224),
                          (480, 224))[::-1]
        self.money = 100

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)

        self.tower_places = []
        self.mobs = []

        self.load_map()

        minion = mobs.Minion(1, self.full_path[0], self.full_path)
        self.mobs.append(minion)

        self.last_spawn_time = pg.time.get_ticks()

    def load_map(self):
        begin = map_components.EnemyPath("begin", self.full_path[0])
        self.all_sprites.add(begin)

        for i in range(7):
            path = map_components.EnemyPath("enemy", self.full_path[i+1])
            self.all_sprites.add(path)

        end = map_components.EnemyPath("end", self.full_path[-1])
        self.all_sprites.add(end)

        base = map_components.TowerPlace((224, 160))
        self.tower_places.append(base)

        base2 = map_components.TowerPlace((228 + 128, 164))
        self.tower_places.append(base2)

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            for tower_place in self.tower_places:
                if tower_place.click_on_it(x, y):
                    if not tower_place.tower:
                        tower_place.set_tower("turret", self.mobs)
                        tower_place.selected = True

    def update(self, keys, now):
        if pg.time.get_ticks() - self.last_spawn_time >= 2000:
            minion = mobs.Minion(1, self.full_path[0], self.full_path)
            self.mobs.append(minion)
            self.last_spawn_time = pg.time.get_ticks()

        self.all_sprites.update()

        for tower_place in self.tower_places:
            tower_place.update()

        for mob in self.mobs:
            if not mob.done: mob.update()
            else:
                if mob.health <= 0:
                    self.money += mob.reward
                self.mobs.remove(mob)

    def draw(self, surface):
        surface.fill((0, 0, 0))

        self.all_sprites.draw(surface)

        for tower_place in self.tower_places:
            tower_place.draw(surface)

        for mob in self.mobs:
            mob.draw(surface)
