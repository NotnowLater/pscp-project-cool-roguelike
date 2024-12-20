""" Define the tiles to be use in GameMap"""
from typing import Tuple

import numpy as np

# Tile graphics structured type compatible with Console.rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    ) -> np.ndarray:
    """ Helper function for defining individual tile types. """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# UNSEEN represents unexplored, unseen tiles, uses to draw unseen tiles.
UNSEEN = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True, 
    transparent=True, 
    dark=(ord("."), (50, 50, 50), (0, 0, 0)),
    light=(ord("."), (80, 80, 80), (0, 0, 0)))
wall = new_tile(
    walkable=False, 
    transparent=False, 
    dark=(ord("↕"), (0, 0, 0), (50, 50, 50)),
    light=(ord("↕"), (255, 255, 255), (150, 150, 169)))
wall2 = new_tile(
    walkable=False, 
    transparent=False, 
    dark=(ord("↕"), (0, 0, 0), (50, 50, 50)),
    light=(ord("↕"), (255, 255, 255), (150, 150, 168)))
up_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("σ"), (50, 50, 50), (0, 0, 0)),
    light=(ord("σ"), (255, 255, 255), (0, 0, 0)),
)
end_switch = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("π"), (50, 50, 50), (0, 0, 0)),
    light=(ord("π"), (255, 255, 255), (0, 0, 0)),
)
