import pygame as pg
import enum

from ..components import ui
from ..constants import COLORS, FONT_PATH, HUD_SPRITES, WIDTH, TOWER_SPRITES
from ..controllers import sound_controller as sc
from ..tools import load_image

TOWERS_COST = {
    "turret": 100,
    "bomber": 150,
    "sniper": 350
}


class HudController(object):
    def __init__(self):
        self.match_hud = MatchHud()
        self.tower_select_hud = TowerHud()
        self.tower_details_hud = None
        self.selected_tower_place = None

    def reset(self):
        self.tower_select_hud = TowerHud()

    def show_tower_select_hud(self, tower_place):
        self.selected_tower_place = tower_place
        self.tower_select_hud.show = True

    def show_tower_details_hud(self, tower):
        pass

    def close_tower_select_hud(self):
        self.tower_select_hud = TowerHud()

    def close_tower_details_hud(self):
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
        self.selected_tower_name = None
        self.highlight = None
        self.font = pg.font.Font(FONT_PATH.as_posix(), 24)
        self.create_hud_buttons()

    def create_hud_buttons(self):
        self.tower_images = []

        turret_image = TowerImage(125, 75, "turret", TOWER_SPRITES["turret"].as_posix())
        bomber_image = TowerImage(275, 75, "bomber", TOWER_SPRITES["bomber"].as_posix())
        sniper_image = TowerImage(425, 75, "sniper", TOWER_SPRITES["sniper"].as_posix())

        self.tower_images.append(turret_image)
        self.tower_images.append(bomber_image)
        self.tower_images.append(sniper_image)

        self.button = pg.sprite.Sprite()
        self.button.image = pg.transform.scale(load_image(HUD_SPRITES["button"], -1)[0], (192, 192))
        self.button.rect = self.button.image.get_rect()
        self.button_position = (750, 30)
        self.button.rect.topleft = (self.button_position[0], self.button_position[1] + 64 * 8)

        self.button_text = self.font.render("BUY", 0, (255, 255, 255))
        self.text_position = (self.button_position[0] + 64, self.button_position[1] + 55)

    def reset_background(self):
        self.screen = pg.transform.scale(load_image(HUD_SPRITES["background"], 0)[0], (1024, 64 * 4))

    def click_on_it(self, x, y):
        return self.show and self.screen_rect.collidepoint(x, y)

    def click_on_button(self, x, y):
        return self.button.rect.collidepoint(x, y)

    def get_click_event_pos(self, x, y):
        if self.click_on_button(x, y):
            if self.selected_tower_name and \
                self.money >= TOWERS_COST[self.selected_tower_name]:
                self.discount = TOWERS_COST[self.selected_tower_name]
                self.done = True
            sc.SoundController().play_button_click()
        else:
            for tower_image in self.tower_images:
                if tower_image.click_on_it(x, y):
                    self.selected_tower_name = tower_image.name
                    pos = (tower_image.rect.topleft[0] - 5, 
                            tower_image.rect.topleft[1] - 5 - 64 * 8)
                    sizes = (106, 106)
                    self.highlight = pg.Rect(pos, sizes)

    def update(self, now, money):
        self.money = money

    def draw(self, surface):
        if self.show: 
            self.reset_background()

            if self.selected_tower_name:
                pg.draw.rect(self.screen, (0, 0, 255), self.highlight)

            for tower_image in self.tower_images:
                tower_image.draw(self.screen)

            self.screen.blit(self.button.image, self.button_position)
            self.screen.blit(self.button_text, self.text_position)
            surface.blit(self.screen, self.screen_rect.topleft)


class TowerImage(pg.sprite.Sprite):
    def __init__(self, x, y, name, image_path):
        super().__init__()
        self.image = pg.transform.scale(load_image(image_path, -1)[0], (96, 96))
        self.rect = self.image.get_rect()
        self.position = (x, y)
        self.rect.topleft = (x, y + 64 * 8)
        self.name = name

    def click_on_it(self, x, y):
        return self.rect.collidepoint(x, y)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.position)
