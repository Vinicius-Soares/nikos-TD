# Elementos de UI do jogo
import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, x, y, title):
        self.x = x
        self.y = y
        self.title = title
