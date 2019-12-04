import pygame as pg

from ..constants import SOUND_PATH


SOUNDS = {
    "mob_death": SOUND_PATH / "mob_death.wav",
    "button_click": SOUND_PATH / "button_click.wav",
    "turret_shot": SOUND_PATH / "turret_shot.wav",
    "bomber_shot": SOUND_PATH / "bomber_shot.wav",
    "sniper_shot": SOUND_PATH / "sniper_shot.wav"
}


class SoundController(object):
    def __init__(self):
        pass

    def play_mob_death(self):
        pg.mixer.Sound(SOUNDS["mob_death"].as_posix()).play()

    def play_button_click(self):
        pg.mixer.Sound(SOUNDS["button_click"].as_posix()).play()

    def play_turret_shot(self):
        pg.mixer.Sound(SOUNDS["turret_shot"].as_posix()).play()

    def play_bomber_shot(self):
        pg.mixer.Sound(SOUNDS["bomber_shot"].as_posix()).play()

    def play_sniper_shot(self):
        pg.mixer.Sound(SOUNDS["sniper_shot"].as_posix()).play()
