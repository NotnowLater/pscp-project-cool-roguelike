""" Define The GameMap """

from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

from entity import Actor, Item

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.engine = engine
        self.entities = set(entities)
        # Create the map array and fill it with Wall.
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.tiles[30:33, 22] = tile_types.wall
        # Tiles that are current visible.
        self.visible = np.full((width, height), fill_value=False, order="F")
        # Tiles that the player have seen
        self.seen = np.full((width, height), fill_value=False, order="F")
        self.upstairs_location = (0, 0)
        self.endswitch_location = (0, 0)

    @property
    def game_map(self) -> GameMap:
        """ Return the game_map. """
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """ Iterate over this maps living actors. """
        yield from(entity for entity in self.entities.copy() if isinstance(entity, Actor) and entity.alive)

    @property
    def items(self) -> Iterator[Item]:
        """" Iterate over this maps items. """
        yield from(entity for entity in self.entities if isinstance(entity, Item))

    def is_in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_actor_at(self, x: int, y: int) -> Optional[Actor]:
        """ Return An Actor at given location. """
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def get_blocking_entity_at(self, x: int, y: int) -> Optional[Entity]:
        """ Return the blocking entity and given location """
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity
        return None

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

        sorted_entities = sorted(self.entities, key=lambda x: x.render_order.value)

        for entity in sorted_entities:
            # Only draw the entities that are in the FOV 
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)
class GameWorld:
   """
   Holds the settings for the GameMap, and generates new maps when moving down the stairs.
   """

   def __init__(
       self,
       *,
       engine: Engine,
       map_width: int,
       map_height: int,
       max_rooms: int,
       room_min_size: int,
       room_max_size: int,
       current_floor: int = 0
   ):
       self.engine = engine

       self.map_width = map_width
       self.map_height = map_height

       self.max_rooms = max_rooms

       self.room_min_size = room_min_size
       self.room_max_size = room_max_size

       self.current_floor = current_floor

   def generate_floor(self) -> None:
       from dungen import generate_dungeon

       self.current_floor += 1

       self.engine.game_map = generate_dungeon(
           max_rooms=self.max_rooms,
           room_min_size=self.room_min_size,
           room_max_size=self.room_max_size,
           map_width=self.map_width,
           map_height=self.map_height,
           engine=self.engine,
       )
