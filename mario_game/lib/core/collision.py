from typing import List, Tuple
import pygame as pg

from lib.core.player import Player
from lib.core.states import CollisionState


def get_pixels_to_bottom(player: Player, sprites: List[pg.sprite.Sprite]) -> int:
    _, player_right, player_bot, player_left = _get_bounds(player)
    smallest = 999999
    for s_top, s_right, _, s_left in map(_get_bounds, sprites):
        if s_left < player_right and s_right > player_left:
            distance = s_top - player_bot
            if distance >= 0:
                smallest = min(smallest, distance)
    return max(0, smallest)

def get_pixels_to_right(player: Player, sprites: List[pg.sprite.Sprite]) -> int:
    player_top, player_right, player_bot, _ = _get_bounds(player)
    smallest = 999999
    for s_top, _, s_bot, s_left in map(_get_bounds, sprites):
        if s_top < player_bot and s_bot > player_top:
            distance = s_left - player_right
            if distance >= 0:
                smallest = min(smallest, distance)
    return max(0, smallest)

def get_pixels_to_left(player: Player, sprites: List[pg.sprite.Sprite]) -> int:
    player_top, _, player_bot, player_left = _get_bounds(player)
    smallest = 999999
    for s_top, s_right, s_bot, _ in map(_get_bounds, sprites):
        if s_top < player_bot and s_bot > player_top:
            distance = player_left - s_right
            if distance >= 0:
                smallest = min(smallest, distance)
    return max(0, smallest)

def _get_bounds(sprite: pg.sprite.Sprite) -> Tuple[int, int, int, int]:
    return sprite.rect.midtop[1], sprite.rect.midright[0], sprite.rect.midbottom[1], sprite.rect.midleft[0]

def compute_collision_states(sprite: pg.sprite.Sprite, 
                             other_sprites: List[pg.sprite.Sprite]) -> List[CollisionState]:
    rect = sprite.rect

    # Expand rectangle to check for proximity
    collision_rect = pg.Rect(rect)
    collision_rect.width += 2
    collision_rect.height += 2
    collision_rect.top -= 1
    collision_rect.left -= 1
    colliding_rects = [o.rect for o in other_sprites if collision_rect.colliderect(o.rect)]

    # Collect states
    states = []
    for other_rect in colliding_rects:
        if rect.midbottom[1] == other_rect.midtop[1]:
            # Player touching ground!
            states.append(CollisionState.BOTTOM)
        elif rect.midtop[1] == other_rect.midbottom[1]:
            # Player touching roof!
            states.append(CollisionState.TOP)
        
        if rect.midleft[0] == other_rect.midright[0]:
            # Player touching its left side
            states.append(CollisionState.LEFT)
        elif rect.midright[0] == other_rect.midleft[0]:
            # Player touching its right side
            states.append(CollisionState.RIGHT)
    return states
