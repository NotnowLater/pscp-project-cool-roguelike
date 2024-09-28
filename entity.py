""" Define the game entity """

from typing import Tuple, TypeVar, TYPE_CHECKING

import copy
# Maybe use this, idk man.
# if TYPE_CHECKING:
#     from game_map import GameMap
from game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
    A generic object to represent entity in the game like player, enemy, item.
    """
    def __init__(
            self, 
            x: int = 0, 
            y: int = 0, 
            char: str = "?", 
            color: Tuple[int, int, int] = (255, 255, 255),
            name = "entity name here",
            blocks_movement = False
            ):
        self.x = x
        self.y = y
        # Char that use to Represent this entity.
        self.char = char
        # Tuple use to define RGB Color to render the entity.
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn_copy(self: T, game_map : GameMap, x : int, y : int):
        """ Spawn a copy of this instance at the given location on the game map. """
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        game_map.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by dx, dy.
        self.x += dx
        self.y += dy