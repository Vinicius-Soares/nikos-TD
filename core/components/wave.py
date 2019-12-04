# Inimigos do jogo
import pygame as pg
from random import randint
from . import mobs

MOBS = [mobs.Minion, mobs.Runner, mobs.Fatman]


class Wave():
    def __init__(self, mobs, path, intervals, now):
        self.mobs = self.create_mobs(mobs, path)
        self.intervals = intervals
        self.time = now
        self.ready = False
        self.finished = False

    def update(self, now):
        self.ready = now >= self.time + self.intervals[0] * 1000
        if self.ready:
            self.time = now

    def next(self):
        next_mob = self.mobs[0]
        self.mobs.pop(0)
        self.intervals.pop(0)
        self.finished = len(self.mobs) == 0
        return next_mob

    def create_mobs(self, new_mobs, path):
        i = 0
        while i < len(new_mobs):
            new_mobs[i] = MOBS[new_mobs[i]-1](1, path[0], path)
            i += 1
        return new_mobs
