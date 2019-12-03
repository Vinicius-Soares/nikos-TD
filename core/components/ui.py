# Elementos de UI do jogo
import pygame as pg

from ..tools import load_image
from ..constants import HUD_SPRITES


class Button(pg.sprite.Sprite):
    def __init__(self, x, y, title):
        self.image = pg.transform.scale(load_image(HUD_SPRITES["button"], -1)[0], (192, 192))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pos = self.rect.topleft
        self.title = title
        self.click = False

    def perform_action(self):
        self.click = True

    def draw(self, surface):
        surface.blit(self.image, self.pos)
