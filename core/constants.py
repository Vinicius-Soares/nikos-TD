import os
import pygame as pg
from pathlib import Path

BASE_PATH = Path()
FONT_PATH = BASE_PATH / 'assets' / 'fonts' / 'Pixeled.ttf'

WIDTH = 1024
HEIGHT = 768
MODE = (WIDTH, HEIGHT)
TITLE = "Niko's Tower Defense"

SPRITE_PATH = BASE_PATH / "sprites"

BACKGROUNDS = {
    "menu" : SPRITE_PATH / "background.png",
    "credits" : SPRITE_PATH / "background.png",
    "gameplay" : SPRITE_PATH / "background.png",
    "gameover" : SPRITE_PATH / "background.png"
}

PATH_TYPES = {
    "begin": SPRITE_PATH / "begin.png",
    "end": SPRITE_PATH / "end.png",
    "enemy": SPRITE_PATH / "enemy_path.png"
}

TOWERPLACE_SPRITE = SPRITE_PATH / 'tower_place.png'

TOWER_SPRITES = {
    "turret": SPRITE_PATH / "turret.png",
    "bomber": SPRITE_PATH / "bomber.png",
    "sniper": SPRITE_PATH / "sniper.png"
}

ENEMY_SPRITES = {
    "minion": SPRITE_PATH / "minion.png",
    "runner": SPRITE_PATH / "runner.png",
    "fatman": SPRITE_PATH / "fatman.png"
}

BULLET_SPRITES = {
    "turret": SPRITE_PATH / "bullet_turret.png",
    "bomber": SPRITE_PATH / "bullet_bomber.png",
    "sniper": SPRITE_PATH / "bullet_sniper.png"
}

COLORS = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'path': (156, 156, 156),
    'base': (100, 100, 100),
    'begin': (0, 255, 0),
    'end': (255, 0, 0),
}
