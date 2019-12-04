'''
  Project Name: Niko's Tower Defense
  Developers: Gabriel San Martin, Victor Yan Pereira, Vinicius Soares
  Year: 2019

  Pixeled Font: https://www.dafont.com/pt/pixeled.font
'''

import pygame as pg
import sys
from core.main import main

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()
