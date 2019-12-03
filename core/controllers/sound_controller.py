import pygame as pg

from ..constants import SOUNDS

class SoundController(object):
    def __init__(self):
        pass

    def play_mob_death(self):
        pg.mixer.Sound(SOUNDS["mob_death"].as_posix()).play()

    def play_turret_shot(self):
        pg.mixer.Sound(SOUNDS["turret_shot"].as_posix()).play()
