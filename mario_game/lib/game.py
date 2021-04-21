from typing import Tuple

import pygame as pg

from lib.core.level import Level
from lib.core.player import Player
from lib.core.states import PlayerState, GameState, CollisionState
from lib.utilities.constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH,
    HEART_WIDTH, HEART_HEIGHT, JUMP_DURATION,
    HEART_IMG_PATH
)


class Game:
    """Class for all game logic."""

    def __init__(self, screen: pg.display, background_color: Tuple[int, int, int],
                 settings: dict):
        self._binds = {}
        self._background_color = background_color
        self._screen = screen
        self._states = {}
        self._player_collisions = [CollisionState.BOTTOM]
        self._current_level = 0
        self._settings = settings
        self._level = self._next_level()
        self._player = Player(
            spawn_x=0,
            spawn_y=SCREEN_HEIGHT - self._level.get_height() - PLAYER_HEIGHT
        )
        self._player_group = pg.sprite.Group()
        self._player_group.add(self._player)
        self._n_lives = 3
        self._heart_image = self._setup_heart_image()

    def _setup_heart_image(self) -> pg.image:
        image = pg.image.load(HEART_IMG_PATH).convert()
        image = pg.transform.scale(image, (HEART_WIDTH, HEART_HEIGHT))
        image.convert_alpha()
        image.set_colorkey((0, 0, 0))
        return image

    def _next_level(self):
        self._current_level += 1
        if self._current_level not in self._settings:
            # THE END
            return None
        try:
            next_level = Level(self._settings[self._current_level])
        except Exception:
            print("Warning! Could not create level, make sure specification is correct.")
            raise
        return next_level

    def setup(self):
        def jump():
            if PlayerState.JUMPING not in self._states and CollisionState.BOTTOM in self._player_collisions:
                self._states[PlayerState.JUMPING] = JUMP_DURATION
        def go_left():
            if CollisionState.LEFT not in self._player_collisions:
                self._player.go_left()
        def go_right():
            if CollisionState.RIGHT not in self._player_collisions:
                self._player.go_right()
        self._add_bind(pg.K_UP, jump)
        self._add_bind(pg.K_LEFT, go_left)
        self._add_bind(pg.K_RIGHT, go_right)

    def _add_bind(self, key, func):
        self._binds[key] = func

    def update(self) -> GameState:
        # Update states
        self._player_collisions = self._level.compute_collisions(self._player)

        # Perform actions depending on pressed keys
        pressed = pg.key.get_pressed()
        for key, func in self._binds.items():
            if pressed[key]:
                func()

        # Perform updates from states
        finished_states = []
        for state, updates_left in self._states.items():
            if state == PlayerState.JUMPING:
                self._player.go_up()
            else:
                raise ValueError("Not implemented...")

            self._states[state] -= 1
            if updates_left == 0:
                finished_states.append(state)
        for state in finished_states:
            del self._states[state]

        # Perform gravity updates
        if PlayerState.JUMPING not in self._states:
            if CollisionState.BOTTOM not in self._player_collisions:
                self._player.go_down()

        # Check player death
        if self._player.get_position()[1] > SCREEN_HEIGHT:
            self._player.reset_position()
            self._n_lives -= 1
            if self._n_lives <= 0:
                return GameState.GAME_OVER

        # Check level complete
        player_x_position = self._player.get_position()[0]
        if player_x_position >= (SCREEN_WIDTH - PLAYER_WIDTH):
            # Level complete, move on to next one
            self._level = self._next_level()
            if self._level is None:
                return GameState.GAME_WIN
            self._player.reset_position()

        # Perform graphics updates
        self._screen.fill(self._background_color)
        self._player_group.draw(self._screen)
        self._level.draw(self._screen)
        heart_x = 5 + HEART_WIDTH
        for _ in range(self._n_lives):
            self._screen.blit(self._heart_image, (SCREEN_WIDTH - heart_x, 5))
            heart_x += 5 + HEART_WIDTH

        return GameState.ONGOING
