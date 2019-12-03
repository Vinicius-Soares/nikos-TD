import pygame as pg
import enum

from ..components import ui
from ..constants import COLORS, FONT_PATH, HUD_SPRITES, WIDTH
from ..tools import load_image


class HudController(object):
    def __init__(self):
        self.match_hud = MatchHud()
        self.tower_select_hud = TowerHud()
        self.selected_tower_place = None

    def reset(self):
        self.tower_hud = TowerHud()

    def click_on_any_hud(self, x, y):
        return self.match_hud.click_on_it(x, y) or \
            self.tower_select_hud.click_on_it(x, y)

    def show_tower_select_hud(self, tower_place):
        self.selected_tower_place = tower_place
        self.tower_select_hud.show = True

    def show_upgrade_tower_hud(self, tower):
        pass

    def close_tower_select_hud(self):
        self.tower_select_hud = TowerHud()

    def close_upgrade_hud(self):
        self.upgrade_hud = None

class MatchHud():
    def __init__(self):
        self.rect = pg.Rect(0, 0, 1024, 64)
        self.font = pg.font.Font(FONT_PATH.as_posix(), 24)
        self.initialize_sprites()

    def initialize_sprites(self):
        self.life_image = pg.transform.scale(load_image(HUD_SPRITES["health"], -1)[0], (48, 48))
        self.money_image = pg.transform.scale(load_image(HUD_SPRITES["coin"], -1)[0], (48, 48))

    def time_x_position(self):
        number_of_letters = len(self.time)
        return (WIDTH / 2) - (number_of_letters // 2 * 16)
    
    def update_time(self, now):
        seconds = now // 1000
        minutes = seconds // 60
        seconds -= minutes * 60
        self.time = repr(minutes).zfill(2) + ":" + repr(seconds).zfill(2)

    def click_on_it(self, x, y):
        return self.rect.collidepoint(x, y)

    def update(self, now, life, money):
        self.life = life
        self.money = money
        self.life_text = self.font.render(repr(self.life), 0, COLORS["white"])
        self.money_text = self.font.render(repr(self.money), 0, COLORS["white"])
        self.update_time(now)
        self.time_text = self.font.render(self.time, 0, COLORS["white"])

    def draw(self, surface):
        surface.blit(self.life_image, (10, 10))
        surface.blit(self.life_text, (65, -7))
        surface.blit(self.money_image, (160, 8))
        surface.blit(self.money_text, (215, -7))
        surface.blit(self.time_text, (self.time_x_position(), -7))


class TowerHud():
    def __init__(self):
        super().__init__()
        self.screen = pg.transform.scale(load_image(HUD_SPRITES["background"], 0)[0], (1024, 64 * 4))
        self.screen_rect = self.screen.get_rect()
        self.screen_rect.topleft = (0, 64 * 8)
        self.show = False
        self.done = False
        self.selected_tower = None
        self.font = pg.font.Font(FONT_PATH.as_posix(), 24)
        
    def click_on_it(self, x, y):
        return self.show and self.screen_rect.collidepoint(x, y)

    def get_event(self, event):
        pass

    def update(self, now, money):
        self.money = money

    def draw(self, surface):
        if self.show: surface.blit(self.screen, self.screen_rect.topleft)
