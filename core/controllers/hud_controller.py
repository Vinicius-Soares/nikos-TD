import pygame as pg

from ..components import ui
from ..constants import COLORS, FONT_PATH, HUD_SPRITES, WIDTH
from ..tools import load_image

class HudController(object):
    def __init__(self):
        self.match_hud = MatchHud()
        self.tower_hud = TowerHud()

    def reset(self):
        self.tower_hud.reset()

    def click_on_any_hud(self, x, y):
        return self.match_hud.click_on_it(x, y) or \
            self.tower_hud.click_on_it(x, y)

    def show_tower_hud(self, tower):
        self.tower_hud.set_tower(tower)

    def get_event(self, event):
        self.tower_hud.get_event(event)

    def update(self, now, life, money):
        self.match_hud.update(now, life, money)
        self.tower_hud.update(now, life, money)

    def draw(self, surface):
        self.match_hud.draw(surface)
        self.tower_hud.draw(surface)


class _Hud(object):
    def __init__(self):
        self.font = pg.font.Font(FONT_PATH.as_posix(), 24)
        self.done = False

    def click_on_it(self, x, y):
        pass

    def update(self, now):
        pass

    def draw(self, surface):
        pass


class MatchHud(_Hud):
    def __init__(self):
        super().__init__()
        self.time = "00:00"
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
        return super().click_on_it(x, y)

    def update(self, now, life, money):
        super().update(now)
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


class TowerHud(_Hud):
    def __init__(self):
        super().__init__()
        self.screen = pg.transform.scale(load_image(HUD_SPRITES["background"], 0)[0], (1024, 64 * 4))
        self.screen_rect = self.screen.get_rect()
        self.screen_rect.topleft = (0, 64 * 8)
        self.show = False
        self.tower = None
        self.initialize_tower_buttons()

    def initialize_tower_buttons(self):
        self.turret_button = ui.Button(10, 10, "Turret")
        self.bomber_button = ui.Button(100, 100, "Bomber")
        self.sniper_button = ui.Button(200, 200, "Sniper")

    def reset(self):
        self.show = False
        self.screen = pg.transform.scale(load_image(HUD_SPRITES["background"], 0)[0], (1024, 64 * 4))

    def set_tower(self, tower):
        self.show = True
        self.tower = tower
        
    def click_on_it(self, x, y):
        return self.show and self.screen_rect.collidepoint(x, y)

    def get_event(self, event):
        pass

    def update(self, now, life, money):
        super().update(now)

    def draw(self, surface):
        if self.show: 
            surface.blit(self.screen, self.screen_rect.topleft)
            if not self.tower:
                self.draw_select_tower(self.screen)
            else:
                self.draw_upgrade_tower(self.screen)

    def draw_select_tower(self, surface):
        self.screen.blit(self.font.render("Towers", 0, COLORS["white"]), (35, 10))
        self.turret_button.draw(self.screen)

    def draw_upgrade_tower(self, surface):
        pass
