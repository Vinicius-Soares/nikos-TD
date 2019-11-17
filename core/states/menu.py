import pygame as pg

from .. import state_machine


class Menu(state_machine._State):
    def __init__(self):
        state_machine._State.__init__(self)
        self.next = "GAMEPLAY"
        self.font = pg.font.Font(None, 50)
        self.text = self.font.render("Hello from Menu. Press ENTER to continue", True, (0, 128, 0))

    def get_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.done = True

    def update(self, keys, now):
        pass

    def draw(self, surface):
        surface.fill((255, 255, 255))
        surface.blit(self.text, (50, 50))
