""" Define The GameMap """

import numpy as np
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        # Create the map array and fill it with Wall.
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.tiles[30:33, 22] = tile_types.wall
        # Tiles that are current visible.
        self.visible = np.full((width, height), fill_value=False, order="F")
        # Tiles that the player have seen
        self.seen = np.full((width, height), fill_value=False, order="F")

    def is_in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """ 
        Render the map to console.
        If tiles is in "visible" array, draw it with its light color.
        If tiles is in "seen" array but not in "visible", draw it with its dark color.
        Otherwise draw the tile with UNSEEN.
        """
        console.rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.seen],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.UNSEEN
        )