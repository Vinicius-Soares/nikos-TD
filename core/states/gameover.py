import pygame as pg

from .. import state_machine


class Gameover(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        self.font = pg.font.Font(None, 50)
        self.text = self.font.render("Perdeu", True, (128, 255, 0))

    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.done = True

    def update(self, keys, now):
        pass

    def draw(self, surface):
        surface.fill((128, 128, 128))
        surface.blit(self.text, (50, 50))
