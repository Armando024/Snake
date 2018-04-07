import pygame as sc
import sys
from Controls import Controls
from intro import Intro
from game import Game
if __name__=='__main__':
    states={
            'Introduction':Intro(),
            'Game':Game()
        }
    sc.key.set_repeat(1,28)
    app=Controls(503,649,60)
    app.setup(states,'Introduction')
    app.main_loop()
    sc.quit()
    sys.exit()









