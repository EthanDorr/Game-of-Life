# Conway's Game of Life
# Written by Ethan Dorr

import os

from game import ConwayGame

# TODO:
    # 1. Add "PAUSED" text when game is paused

# IDEAS:
    # 1. Allow for different resolutions in some sort of main menu
    # 2. Allow a way to save different patterns and deploy them later (sounds complicated)

def main():
    game = ConwayGame(paused = True)
    game.run()

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    main()
