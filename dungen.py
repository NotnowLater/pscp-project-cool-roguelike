""" The Dugeon Generation """

from __future__ import annotations

from typing import Tuple
from game_map import GameMap
import tile_types
import random
import tcod
from typing import Iterator, Tuple, TYPE_CHECKING, List

if TYPE_CHECKING:
    from entity import Entity

class RectangularRoom:
    """ A Class that define a Rectangular Room For Dungeon Generation"""
    def __init__(self, x: int, y: int, width: int, height: int):
        # top left positions
        self.x1 = x
        self.y1 = y
        # bottom right position
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """Return the center point of the room """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        # Add 1 to x1 and y1 to ensure that there is always a wall.
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)
    
    def check_intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

def make_tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """ Return an L-shaped tunnel between these two points. """
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2
    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def generate_dungeon(
        max_rooms: int, room_min_size: int, room_max_size: int,
        map_width: int, map_height: int, player: Entity,
    ) -> GameMap:
    """ Return The Generated Dungeon of given size. """
    dungeon = GameMap(map_width, map_height)
    rooms: List[RectangularRoom] = []
    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)
        # Check through the other rooms and see if they intersect with this one.
        if any(new_room.check_intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.

        # No intersects, The Room is Valid, Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor
        # Put the player in the center of the first room
        if len(rooms) == 0:
            player.x, player.y = new_room.center
        else:
            # Dig out a tunnel between this room and the last one.
            for x, y in make_tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
        # Append the new room to the list.
        rooms.append(new_room)
    return dungeon
