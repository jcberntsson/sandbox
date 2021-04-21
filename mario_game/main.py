"""
Main-file for Mario-inspired platform game.
"""
from typing import Tuple
import pygame as pg
import numpy as np
import yaml

from lib.game import Game
from lib.core.states import GameState
from lib.utilities.constants import (
    ORANGE, SKY_BLUE, BLACK,
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT,
    LEVELS_PATH
)

SCREEN_SIZE = np.array([SCREEN_WIDTH, SCREEN_HEIGHT])
PLAYER_SIZE = np.array([PLAYER_WIDTH, PLAYER_HEIGHT])

TILE_SIZE = 64


def _setup_text(string: str) -> Tuple:
    font = pg.font.SysFont('Arial', 32)
    text = font.render(string, True, ORANGE)
    rect = text.get_rect()
    rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    return text, rect

def main():
    # Setup pygame models
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    screen.fill(SKY_BLUE)
    pg.display.set_caption('The no-name game')
    clock = pg.time.Clock()

    # Read settings
    with open(LEVELS_PATH, 'r') as stream:
        settings = yaml.safe_load(stream)

    # Setup internal models
    game = Game(screen, SKY_BLUE, settings)
    game.setup()

    # Setup texts
    texts = {
        GameState.GAME_OVER: _setup_text("GAME OVER"),
        GameState.GAME_WIN: _setup_text("YOU WON!")
    }

    # Run game loop
    state = GameState.ONGOING
    while True:
        # Check for quit event
        if any([event.type == pg.QUIT for event in pg.event.get()]):
            break
    
        # Run game update depending on previous state
        if state == GameState.ONGOING:
            state = game.update()
        else:
            screen.fill(BLACK)
            screen.blit(*texts[state])

        # Tick game engine
        pg.display.update()
        clock.tick(300)

    # Quit pygame and script
    pg.quit()
    quit()


if __name__ == "__main__":
    main()
