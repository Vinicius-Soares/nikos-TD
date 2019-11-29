import pygame as pg

from .. import state_machine
from ..components import map_components, mobs, towers
from ..tools import load_image
from ..constants import PATH_TYPES, TOWERPLACE_SPRITE

class Gameplay(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        self.all_sprites = pg.sprite.Group()
        self.full_path = ((96, 160),
                          (96, 224),
                          (96, 288),
                          (160, 288),
                          (224, 288),
                          (288, 288),
                          (352, 288),
                          (416, 288),
                          (480, 288))[::-1]
        self.money = 100

        self.hud_controller = HudController()

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
        base2.set_tower("turret", self.mobs)
        self.tower_places.append(base2)

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            click_on_any_hud = self.hud_controller.click_on_match_hud(x, y) or \
                self.hud_controller.click_on_tower_hud(x, y)
            if not click_on_any_hud:
                self.hud_controller.reset()
                for tower_place in self.tower_places:
                    if tower_place.click_on_it(x, y):
                        self.hud_controller.show_tower_hud(tower_place.tower)
                        '''
                        if not tower_place.tower:
                            tower_place.set_tower("turret", self.mobs)
                            tower_place.selected = True
                        '''

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
        
        self.hud_controller.update(now)

    def draw(self, surface):
        surface.fill((0, 0, 0))

        self.all_sprites.draw(surface)

        for tower_place in self.tower_places:
            tower_place.draw(surface)

        for mob in self.mobs:
            mob.draw(surface)

        self.hud_controller.draw(surface)


class HudController():
    def __init__(self):
        self.match_hud = pg.Surface((1024, 64))
        self.tower_hud = pg.Surface((1024, 64 * 4))
        self.match_hud_rect = self.match_hud.get_rect()
        self.tower_hud_rect = self.tower_hud.get_rect()
        self.match_hud_rect.topleft = (0, 0)
        self.tower_hud_rect.topleft = (0, 64 * 8)
        self.tower_hud_color = 0 # Só pra teste
        self.show = False

    def reset(self):
        self.show = False

    def initialize(self, money):
        pass

    def click_on_match_hud(self, x, y):
        return self.match_hud_rect.collidepoint(x, y)

    def click_on_tower_hud(self, x, y):
        return self.show and self.tower_hud_rect.collidepoint(x, y)

    def show_tower_hud(self, tower):
        self.show = True
        if not tower: self.tower_hud_color = (255, 0, 0)
        else: self.tower_hud_color = (0, 0, 255)

    def update(self, now):
        pass

    def draw(self, surface):
        self.match_hud.fill((0, 255, 0))
        surface.blit(self.match_hud, self.match_hud_rect.topleft)
        if self.show:
            self.tower_hud.fill(self.tower_hud_color)
            surface.blit(self.tower_hud, self.tower_hud_rect.topleft)
