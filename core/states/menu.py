import pygame as pg
from ..constants import WIDTH
from .. import state_machine


class Menu(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        text_color = (128, 255, 0)
        self.next = "GAMEPLAY"
        self.font = pg.font.Font(None, 50)
        self.text = self.font.render("Hello from Menu. Press ENTER to continue", True, text_color)
        self.cursor = {
            "font" : self.font.render(">", True, text_color),
            "cors": [350, 200],
            "index": 0
        }
        self.options = [
            {"text":"Novo jogo", "value":"GAMEPLAY"},
            {"text":"Créditos", "value":"CREDITS"},
            {"text":"Sair", "value":"SAIR"}
        ]
        for (index, option) in enumerate(self.options):
            option["font"] = self.font.render(option["text"], True, text_color)
            (x, y) = option["font"].get_width(), (index+2)*100
            x = (WIDTH - x) / 2
            option["cors"] = (x,y)

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.next = self.options[self.cursor["index"]]["value"]
                if self.next == "SAIR": pg.quit()
                else: self.done = True
            if event.key == pg.K_DOWN:
                if self.cursor["index"] < 2: self.cursor["index"]+=1
                else: self.cursor["index"] = 0
                self.cursor["cors"][1] = (self.cursor["index"]+2)*100
            if event.key == pg.K_UP:
                if self.cursor["index"] > 0: self.cursor["index"]-=1
                else: self.cursor["index"] = 2
                self.cursor["cors"][1] = (self.cursor["index"]+2)*100

    def update(self, keys, now):
        pass

    def draw(self, surface):
        surface.fill((128, 128, 128))
        surface.blit(self.text, (50, 50))
        surface.blit(self.cursor["font"], self.cursor["cors"])
        for option in self.options:
            surface.blit(option["font"], option["cors"])
