import os
import pygame as pg

from pathlib import Path
from pygame.image import load
from pygame import error, RLEACCEL

BASE_PATH = Path()
FONT_PATH = BASE_PATH / 'assets' / 'fonts' / 'Pixeled.ttf'

WIDTH = 1024
HEIGHT = 768
MODE = (WIDTH, HEIGHT)
TITLE = "Niko's Tower Defense"

BEGIN_SPRITE = BASE_PATH / 'sprites' / 'begin.png'
END_SPRITE = BASE_PATH / 'sprites' / 'end.png'
ENEMYPATH_SPRITE = BASE_PATH / 'sprites' / 'enemy_path.png'

PATH_TYPES = {
    "begin": BEGIN_SPRITE,
    "end": END_SPRITE,
    "enemy": ENEMYPATH_SPRITE
}

TOWERPLACE_SPRITE = BASE_PATH / 'sprites' / 'tower_place.png'

TURRET_SPRITE = BASE_PATH / 'sprites' / 'turret.png'
BOMBER_SPRITE = BASE_PATH / 'sprites' / 'bomber.html'
SNIPER_SPRITE = BASE_PATH / 'sprites' / 'sniper.html'


MINION_SPRITE = BASE_PATH / 'sprites' / 'minion.png'
RUNNER_SPRITE = BASE_PATH / 'sprites' / 'runner.html'
FATMAN_SPRITE = BASE_PATH / 'sprites' / 'fatman.html'

BULLET_SPRITE = BASE_PATH / 'sprites' / 'bullet_turret.png'

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


def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    try:
        image = load(fullname)
    except error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
