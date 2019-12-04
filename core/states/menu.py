import pygame as pg
import sys

from  ..tools import load_image
from ..constants import WIDTH, MODE, FONT_PATH, BACKGROUNDS, HUD_SPRITES
from .. import state_machine


class Menu(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        
        self.background = pg.transform.scale(load_image(BACKGROUNDS["menu"], -1)[0], MODE)
        self.button = pg.transform.scale(load_image(HUD_SPRITES["button"], -1)[0], (500, 210))

        self.button = {
            "sprite" : self.button,
            "cors": [250, 155],
            "index": 0
        }

        text_color = (128, 255, 0)
        self.next = "GAMEPLAY"
        self.font = pg.font.Font(FONT_PATH.as_posix(), 40)

        title_font = self.font.render("NIKOS  TOWERDEFENSE", True, text_color)
        self.title = {
            "font": title_font,
            "cors": ((WIDTH-title_font.get_width())/2, 50)
        }

        self.cursor = {
            "font" : self.font.render("o", True, text_color),
            "cors": [300, 200],
            "index": 0
        }

        self.options = [
            {"text": "NOVO  JOGO", "value": "GAMEPLAY"},
            {"text": "CRÉDITOS", "value": "CREDITS"},
            {"text": "SAIR", "value": "SAIR"}
        ]

        for (index, option) in enumerate(self.options):
            option["font"] = self.font.render(option["text"], True, text_color)
            (x, y) = option["font"].get_width(), (index+2)*100
            x = (WIDTH - x) / 2
            option["cors"] = (x,y)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.next = self.options[self.button["index"]]["value"]
                if self.next == "SAIR": 
                    pg.quit()
                    sys.exit()
                else: self.done = True
            if event.key == pg.K_DOWN:
                if self.button["index"] < 2: self.button["index"]+=1
                else: self.button["index"] = 0
                self.button["cors"][1] = (self.button["index"]+2)*100-45
            if event.key == pg.K_UP:
                if self.button["index"] > 0: self.button["index"]-=1
                else: self.button["index"] = 2
                self.button["cors"][1] = (self.button["index"]+2)*100-45

    def update(self, keys, now):
        pass

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.title["font"], self.title["cors"])
        surface.blit(self.button["sprite"], self.button["cors"])
        for option in self.options:
            surface.blit(option["font"], option["cors"])
