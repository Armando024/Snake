import pygame as sc
import sys
from gui.Controls import Controls
from gui.intro import Intro
from gui.game import Game
if __name__=='__main__':
    states={
            'Introduction':Intro(),
            'Game':Game()
        }
#    sc.key.set_repeat(1,28)
    app=Controls(503,679,60) #old h is 649
    app.setup(states,'Introduction')
    app.main_loop()
    sc.quit()
    sys.exit()









