import pygame as pg
from ..constants import WIDTH, FONT_PATH

from .. import state_machine


class Credits(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "MENU"
        self.text = ["UNIVERSIDADE  ESTADUAL  DO  AMAZONAS - UEA",
                     "BACHARELADO EM SISTEMAS DE INFORMAÇÃO", "",
                     "LABORATÓRIO DE PROGRAMAÇÃO DE COMPUTADORES",
                     "BACHARELADO EM SISTEMAS DE INFORMAÇÃO",
                     "PROF.DR. JUCIMAR JR", "",
                     "- GABRIEL SENA SAN MARTIN",
                     "- VICTOR YAN PEREIRA E LIMA",
                     "- VINICIUS SOARES DA COSTA"]
        self.text_color = (128, 255, 0)
        self.font = pg.font.Font(FONT_PATH.as_posix(), 24)

    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.done = True

    def update(self, keys, now):
        pass

    def draw(self, surface):
        surface.fill((128, 128, 128))
        for i, line in enumerate(self.text):
            surface.blit(self.font.render(
                line, True, self.text_color), (40, i*50))
