# Elementos de UI do jogo
import pygame as pg

class _Button(pg.sprite.Sprite):
    def __init__(self, text, color, text_color):
        pg.sprite.Sprite.__init__(self)
        self.text = text
        self.color = color
        self.text_color = text_color

    def update(self):
        pass

    def draw(self):
        pass

class _Hud(pg.Rect):
    def __init__(self, pos, width, length):
        pg.Rect.__init__(self, pos, width, length)

    def update(self):
        pass

    def draw(self):
        pass
