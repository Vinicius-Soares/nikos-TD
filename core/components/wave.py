# Inimigos do jogo
import pygame as pg
from random import randint


class Wave():
    def __init__(self, mobs, intervals, now):
        self.mobs = mobs
        self.intervals = intervals
        self.time = now

    def update(self, now):
        pass

    def next(self):
        next_mob = self.mobs[0]
        self.mobs.remove(0)
        self.intervals.remove(0)
        return next_mob
