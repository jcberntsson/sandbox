import os

# Paths
GAME_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
LEVELS_PATH = os.path.join(GAME_ROOT, "settings", "levels.yaml")
GROUND_IMG_PATH = os.path.join(GAME_ROOT, "images", "ground.png")
HEART_IMG_PATH = os.path.join(GAME_ROOT, "images", "heart.png")
PLAYER_IMG_PATH = os.path.join(GAME_ROOT, "images", "player.png")

# Colors
WHITEISH = (255, 255, 255)
ORANGE = (100, 50, 0)
SKY_BLUE = (31, 133, 222)
BLACK = (0, 0, 0)

# Gameplay
STEP_SIZE = 1
JUMP_DURATION = 40

# Sizes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = PLAYER_HEIGHT = 48
HEART_WIDTH = HEART_HEIGHT = 30
