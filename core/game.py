import pygame as pg
from .utils import COLORS, HEIGHT, MODE, TITLE, WIDTH


class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(MODE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        begin = pg.sprite.Sprite()
        begin.image = pg.Surface((100, 100))
        begin.image.fill(COLORS['begin'])
        begin.rect = begin.image.get_rect()
        begin.rect.center = (100, HEIGHT / 2)
        self.all_sprites.add(begin)

        for i in range(8):
            path = pg.sprite.Sprite()
            path.image = pg.Surface((100, 100))
            path.image.fill(COLORS['path'])
            path.rect = path.image.get_rect()
            path.rect.center = (190 + (i * 100), HEIGHT / 2)
            self.all_sprites.add(path)

        end = pg.sprite.Sprite()
        end.image = pg.Surface((100, 100))
        end.image.fill(COLORS['end'])
        end.rect = end.image.get_rect()
        end.rect.center = (900, HEIGHT / 2)
        self.all_sprites.add(end)

        base = pg.sprite.Sprite()
        base.image = pg.Surface((100, 100))
        base.image.fill(COLORS['base'])
        base.rect = base.image.get_rect()
        base.rect.center = (WIDTH / 2, 500)
        self.all_sprites.add(base)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.playing = not self.playing
                self.running = not self.running

    def update(self):
        pass

    def draw(self):
        self.screen.fill(COLORS['black'])
        self.all_sprites.draw(self.screen)
        pg.display.flip()
