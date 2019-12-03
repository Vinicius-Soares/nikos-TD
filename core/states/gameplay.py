import pygame as pg

from .. import state_machine
from ..components import map_components, mobs, towers
from ..controllers import hud_controller as hc
from ..constants import PATH_TYPES, TOWERPLACE_SPRITE, BACKGROUNDS, MODE
from ..tools import load_image

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
        self.life = 5
        self.money = 100

        self.background = pg.transform.scale(load_image(BACKGROUNDS["gameplay"], -1)[0], MODE)
        self.hud_controller = hc.HudController()

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)

        self.tower_places = []
        self.mobs = []

        self.load_map()

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

        #self.tower_places[1].set_tower("turret")

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            if not self.hud_controller.click_on_any_hud(x, y):
                self.hud_controller.close_tower_select_hud()
                self.hud_controller.close_upgrade_hud()
                for tower_place in self.tower_places:
                    if tower_place.click_on_it(x, y):
                        if not tower_place.tower:
                            self.hud_controller.show_tower_select_hud(tower_place)
                            tower_place.selected = True
                        else:
                            self.hud_controller.show_upgrade_tower_hud(tower_place.tower)
                        '''
                            Para testes
                        '''
                        if not tower_place.tower: 
                            tower_place.set_tower("turret")
            else: 
                pass
                '''
                self.hud_controller.get_event(event)
                if self.hud_controller.tower_hud.done:
                    selected_tower = self.hud_controller.tower_hud.selected_tower
                    tower_name = selected_tower.name
                    tower_cost = selected_tower.cost
                    self.hud_controller.selected_tower_place.set_tower(tower_name)
                    self.money -= tower_cost
                '''

    def update(self, keys, now):
        if self.life == 0:
            self.next = "GAMEOVER"
            self.done = True

        if pg.time.get_ticks() - self.last_spawn_time >= 2000:
            minion = mobs.Minion(1, self.full_path[0], self.full_path)
            self.mobs.append(minion)
            self.last_spawn_time = pg.time.get_ticks()

        self.all_sprites.update()

        for tower_place in self.tower_places:
            tower_place.update(now, self.mobs)

        for mob in self.mobs:
            if not mob.done: mob.update()
            else:
                if mob.health <= 0:
                    self.money += mob.reward
                else:
                    self.life -= mob.damage
                    if self.life < 0: self.life = 0
                self.mobs.remove(mob)
        
        self.hud_controller.match_hud.update(now, self.life, self.money)
        self.hud_controller.tower_select_hud.update(now, self.money)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        self.all_sprites.draw(surface)

        for tower_place in self.tower_places:
            tower_place.draw(surface)

        for mob in self.mobs:
            mob.draw(surface)

        self.hud_controller.match_hud.draw(surface)
        self.hud_controller.tower_select_hud.draw(surface)
