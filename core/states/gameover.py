import pygame as pg

from .. import state_machine
from ..constants import MODE, WIDTH, FONT_PATH, BACKGROUNDS, HUD_SPRITES
from ..tools import load_image

class Gameover(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        
        self.background = pg.transform.scale(load_image(BACKGROUNDS["menu"], -1)[0], MODE)
        self.button = pg.transform.scale(load_image(HUD_SPRITES["button"], -1)[0], (550, 210))

        self.button = {
            "sprite" : self.button,
            "cors": [235, 455],
            "index": 0
        }

        self.font = pg.font.Font(FONT_PATH.as_posix(), 40)
        text_color = (128, 255, 0)
        
        title_font = self.font.render("YOU LOSE", True, text_color)
        self.title = {
            "font": title_font,
            "cors": ((WIDTH-title_font.get_width())/2, 200)
        }
        
        self.options = [
            {"text": "VOLTAR AO MENU", "value": "MENU"}
        ]

        for (index, option) in enumerate(self.options):
            option["font"] = self.font.render(option["text"], True, text_color)
            (x, y) = option["font"].get_width(), (index+5)*100
            x = (WIDTH - x) / 2
            option["cors"] = (x,y)

    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.done = True
        
            if event.key == pg.K_RETURN:
                self.next = self.options[self.button["index"]]["value"]
                self.done = True
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
