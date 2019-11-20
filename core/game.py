import pygame as pg

from . import state_machine
from .utils import MODE, TITLE

class Control(object):
    def __init__(self):
        self.initialize()
        self.done = False
        self.clock = pg.time.Clock()
        self.now = 0.0
        self.keys = pg.key.get_pressed()
        self.state_machine = state_machine.StateMachine()

    def initialize(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(MODE)
        pg.display.set_caption(TITLE)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state_machine.get_event(event)


    def update(self):
        self.now = pg.time.get_ticks()
        self.state_machine.update(self.keys, self.now)

    def draw(self):
        if not self.state_machine.state.done:
            self.state_machine.draw(self.screen)
            pg.display.flip()

    def main(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
