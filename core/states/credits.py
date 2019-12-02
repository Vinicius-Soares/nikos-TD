import pygame as pg
from ..constants import WIDTH, FONT_PATH

from .. import state_machine


class Credits(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        self.font = pg.font.Font(FONT_PATH.as_posix(), 30)
        self.text = self.font.render("UNIVERSIDADE  ESTADUAL  DO  AMAZONAS", True, (128, 255, 0))

    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.done = True

    def update(self, keys, now):
        pass

    def draw(self, surface):
        surface.fill((128, 128, 128))
        surface.blit(self.text, (50, 50))
