import pygame as pg
from utils import *

pg.init()
pg.mixer.init()
screen = pg.display.set_mode(MODE)
pg.display.set_caption(TITLE)

running = True

while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False

  screen.fill(BLACK)
  pg.display.flip()