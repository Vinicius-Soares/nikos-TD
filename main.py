import pygame as pg
from utils import *
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
    teste = pg.sprite.Sprite()
    teste.image = pg.Surface((30, 30))
    teste.image.fill(WHITE)
    teste.rect = teste.image.get_rect()
    teste.rect.center = (100, 100)
    self.all_sprites.add(teste)
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
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    pg.display.flip()

g = Game()
while g.running:
  g.new()