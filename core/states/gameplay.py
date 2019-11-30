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
        #self.full_path = ((2, 3),(2, 4),(2, 5),(3, 5),(4, 5),(5, 5),(6, 5),(7, 5),(8, 5))[::-1]
        self.full_path = ((7, 2), (7, 3), (6, 3), (5, 3), (4, 3), (3, 3), (2, 3),
                          (2, 4), (2, 5), (2, 6), (2, 7), (3, 7), (4, 7), (5, 7), (5, 6),
                          (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5),
                          (12, 6), (12, 7), (13, 7), (14, 7), (15, 7), (15, 6), (15, 5),
                          (15, 4), (15, 3), (14, 3), (13, 3), (12, 3), (11, 3), (10, 3), (10, 2))
        self.full_path = [(x*64-32,y*64-32) for (x,y) in self.full_path]

        self.tower_positions = ((2, 2),(4, 5),(6, 6), (15, 2),(13, 5),(11, 6))
        self.tower_positions = [(x*64-32,y*64-32) for (x,y) in self.tower_positions]
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

        for i in range(len(self.full_path)-2):
            path = map_components.EnemyPath("enemy", self.full_path[i+1])
            self.all_sprites.add(path)

        end = map_components.EnemyPath("end", self.full_path[-1])
        self.all_sprites.add(end)

        for coord in self.tower_positions:
            base = map_components.TowerPlace(coord)
            self.tower_places.append(base)

        self.tower_places[-1].set_tower("turret", self.mobs)

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
                        tower_place.selected = True
                        if not tower_place.tower: 
                            tower_place.set_tower("turret", self.mobs) # Apenas para testes

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
        self.money = money

    def update_money(self, value):
        # Usado para comprar torres também
        # Ex: hud_controller.update_money(-cost), 
        # onde cost é o custo da torre
        self.money += value

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
