from enum import Enum

class PlayerState(Enum):
    JUMPING = 1
    ATTACKING = 2

class GameState(Enum):
    ONGOING = 1
    EXITED = 2
    GAME_OVER = 3
    GAME_WIN = 4

class CollisionState(Enum):
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3
    TOP = 4
