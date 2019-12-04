import pygame as pg

from .. import state_machine
from ..components import map_components, mobs, towers, wave
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

        self.tower_positions = ((2, 2),(3,2),(4,2),(4, 5),(3,5),(3,6),(4,6),(6, 6), (15, 2),(14,2),
                                (13,2),(13, 5),(14,5),(13,6),(14,6),(11, 6),(11,7),(10,6),(9,6),(8,6),
                                (7,6),(6,7))
        self.tower_positions = [(x*64-32,y*64-32) for (x,y) in self.tower_positions]
        self.life = 25
        self.money = 500

        self.background = pg.transform.scale(load_image(BACKGROUNDS["gameplay"], -1)[0], MODE)
        self.hud_controller = hc.HudController()

    def startup(self, now, persistant):
        state_machine._State.startup(self, now, persistant)

        self.tower_places = []
        self.mobs = []

        self.load_map()

        now = pg.time.get_ticks()

        self.last_enemy_spawn_time = now
        
        self.waves, self.current_wave = [], 0
        
        self.waves_intervals = [1, 0]

        wave_mobs = [1, 2, 3, 1, 2, 3, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2]
        intervals = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        new_wave = wave.Wave(wave_mobs, self.full_path, intervals, now)
        self.waves.append(new_wave)

        wave_mobs = [3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1]
        intervals = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        new_wave = wave.Wave(wave_mobs, self.full_path, intervals, now)
        self.waves.append(new_wave)

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
            if self.hud_controller.tower_select_hud.click_on_it(x, y):
                self.hud_controller.tower_select_hud.get_click_event_pos(x, y)
            #elif self.hud_controller.tower_details_hud.click_on_it(x, y):
            else:
                self.hud_controller.close_tower_select_hud()
                self.hud_controller.close_tower_details_hud()
                for tower_place in self.tower_places:
                    if tower_place.click_on_it(x, y):
                        if not tower_place.tower:
                            self.hud_controller.show_tower_select_hud(tower_place)
                            tower_place.selected = True
                        else:
                            self.hud_controller.show_tower_details_hud(tower_place.tower)

    def update(self, keys, now):
        if self.life == 0:
            self.next = "GAMEOVER"
            self.done = True

        now = pg.time.get_ticks()

        if self.current_wave < len(self.waves):
            current_wave = self.waves[self.current_wave]

            if current_wave.finished:

                if  (now >= self.last_enemy_spawn_time + self.waves_intervals[self.current_wave] * 1000):
                    self.current_wave+=1 
            else:
                current_wave.update(now)
                if current_wave.ready:
                    self.last_enemy_spawn_time = now
                    self.mobs.append(current_wave.next())

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

        if self.hud_controller.tower_select_hud.done:
            tower_name = self.hud_controller.tower_select_hud.selected_tower_name
            self.hud_controller.selected_tower_place.set_tower(tower_name)
            self.money -= self.hud_controller.tower_select_hud.discount
            self.hud_controller.close_tower_select_hud()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        self.all_sprites.draw(surface)

        for tower_place in self.tower_places:
            tower_place.draw(surface)

        for mob in self.mobs:
            mob.draw(surface)

        self.hud_controller.match_hud.draw(surface)
        self.hud_controller.tower_select_hud.draw(surface)
