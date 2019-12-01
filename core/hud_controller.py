import pygame as pg

from .constants import COLORS, FONT_PATH, HUD_SPRITES, WIDTH
from .tools import load_image

class HudController(object):
    def __init__(self):
        self.match_hud = MatchHud()
        self.tower_hud = TowerHud()

    def reset(self):
        self.tower_hud.reset()

    def initialize(self, money):
        self.match_hud.update_money(money)

    def click_on_any_hud(self, x, y):
        return self.match_hud.click_on_it(x, y) or \
            self.tower_hud.click_on_it(x, y)

    def show_tower_hud(self, tower):
        self.tower_hud.set_tower(tower)

    def update(self, now):
        self.match_hud.update(now)
        self.tower_hud.update(now)

    def draw(self, surface):
        self.match_hud.draw(surface)
        self.tower_hud.draw(surface)


class _Hud(object):
    def __init__(self, x, y, width, length):
        self.screen = pg.Surface((width, length))
        self.screen_rect = self.screen.get_rect()
        self.screen_rect.topleft = (x, y)
        self.font = pg.font.Font(None, 64)
        self.color = 0
        self.done = False

    def click_on_it(self, x, y):
        return self.screen_rect.collidepoint(x, y)

    def update(self, now):
        pass

    def draw(self, surface):
        if not self.done:
            self.screen.fill(self.color)
            surface.blit(self.screen, self.screen_rect.topleft)


class MatchHud(_Hud):
    def __init__(self):
        super().__init__(0, 0, 1024, 64)
        self.color = (255, 255, 255)
        self.life = 100
        self.money = 0
        self.time = "00:00"
        self.initialize_sprites()

    def initialize_texts(self):
        self.life_text = self.font.render(repr(self.life), 0, (0, 0, 0))
        self.money_text = self.font.render(repr(self.money), 0, (0, 0, 0))
        self.time_text = self.font.render(self.time, 0, (0, 0, 0))

    def initialize_sprites(self):
        self.life_image = pg.transform.scale(load_image(HUD_SPRITES["health"])[0], (48, 48))
        self.money_image = load_image(HUD_SPRITES["coin"])[0]

    def time_x_position(self):
        number_of_letters = len(self.time)
        return (WIDTH / 2) - (number_of_letters // 2 * 16)

    def update_money(self, value):
        # Usado para comprar torres também
        # Ex: hud_controller.update_money(-cost), 
        # onde cost é o custo da torre
        self.money += value
    
    def update_time(self, now):
        seconds = now // 1000
        minutes = seconds // 60
        seconds -= minutes * 60
        self.time = repr(minutes).zfill(2) + ":" + repr(seconds).zfill(2)

    def click_on_it(self, x, y):
        return super().click_on_it(x, y)

    def update(self, now):
        super().update(now)
        self.life_text = self.font.render(repr(self.life), 0, (0, 0, 0))
        self.money_text = self.font.render(repr(self.money), 0, (0, 0, 0))
        self.update_time(now)
        self.time_text = self.font.render(self.time, 0, (0, 0, 0))

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.life_image, (10, 10))
        # surface.blit(self.life_text, (10, 10))
        # surface.blit(self.money_text, (120, 10))
        # surface.blit(self.time_text, (self.time_x_position(), 10))


class TowerHud(_Hud):
    def __init__(self):
        super().__init__(0, 64 * 8, 1024, 64 * 4)
        self.show = False
        self.tower = None

    def reset(self):
        self.show = False

    def set_tower(self, tower):
        self.show = True
        self.tower = tower
        self.color = (255, 0, 0) if self.tower else (0, 0, 255)
        
    def click_on_it(self, x, y):
        return self.show and super().click_on_it(x, y)

    def update(self, now):
        super().update(now)

    def draw(self, surface):
        if self.show: 
            super().draw(surface)
