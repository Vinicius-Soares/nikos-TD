import pygame as pg

background_colour = (0,0,0)
(width, height) = (800, 600)

pg.init()
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Niko's Tower Defense")
screen.fill(background_colour)
pg.display.flip()

running = True

while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False