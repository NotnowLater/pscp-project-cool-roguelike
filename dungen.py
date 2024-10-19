""" The Dugeon Generation """

from __future__ import annotations

from typing import Tuple
from game_map import GameMap
import tile_types
import entity_factory
import random
import tcod
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from components.equipment import Equipment

#(Floor, Max Item)
max_items_by_floor = [
    (1, 2),
    (4, 2),
]

#(Floor, Max Monsters)
max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

item_box_chance: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factory.bandage, 25), (entity_factory.ammo20, 70), (entity_factory.flash_grenade, 5)],
    1: [(entity_factory.flash_grenade, 25), (entity_factory.sword, 10),
        (entity_factory.explosive_grenade, 5), (entity_factory.bandage, 20),
        (entity_factory.ammo20, 10)],
}

item_chance: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factory.bandage, 25), (entity_factory.ammo20, 75)],
    2: [(entity_factory.flash_grenade, 25), (entity_factory.sword, 5)],
    4: [(entity_factory.explosive_grenade, 25), (entity_factory.chain_mail, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factory.orc, 50), (entity_factory.security, 20), (entity_factory.item_box, 1)],
    3: [(entity_factory.troll, 15), (entity_factory.item_box, 3)],
    5: [(entity_factory.troll, 30), (entity_factory.item_box, 5)],
    7: [(entity_factory.troll, 60)],
}

def get_max_value_for_floor(
        weighted_chances_by_floor: List[Tuple[int , int]], floor: int
) -> int:
    current_value = 0

    for floor_minimum, value in weighted_chances_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value

def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities

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

def item_box_drop_item(entity: Entity, dungeon: GameMap, box_type: int) -> None:
    """Drop random items when item box is destroyed."""
    
    #random dropped item
    items = random.choices(
            [value[0] for value in item_box_chance[box_type]],
            weights=[value[1] for value in item_box_chance[box_type]],
            k=1
            )
    
    items[0].spawn_copy(dungeon, entity.x, entity.y)

def entity_drop_item(entity: Entity, dungeon: GameMap, equipment: Equipment, drop_chance: float) -> None:
    """Drop random items when enemy is die."""

    #return if you unlucky T-T
    if random.random() > drop_chance:
        return
    
    items_to_drop = []
    if equipment.weapon:
        items_to_drop.append(equipment.weapon)
    if equipment.armor:
        items_to_drop.append(equipment.armor)

    #random dropped item
    if items_to_drop:
        items_to_drop = random.choice(items_to_drop)
        items_to_drop.spawn_copy(dungeon, entity.x, entity.y)


def place_entities(room : RectangularRoom, dungeon: GameMap, floor_number : int,) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )
    monsters: List[Entity] = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        item_chance, number_of_items, floor_number
    )

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        # Check if the entity is overlapping the existing entity first before placing it.
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn_copy(dungeon, x, y)

def generate_dungeon(
        max_rooms: int, room_min_size: int, room_max_size: int,
        map_width: int, map_height: int, engine: Engine,
    ) -> GameMap:
    """ Return The Generated Dungeon of given size. """
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms: List[RectangularRoom] = []
    center_of_last_room = (0, 0)
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
            player.place_at(*new_room.center, dungeon)
        else:
            # Dig out a tunnel between this room and the last one.
            for x, y in make_tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
            center_of_last_room = new_room.center
        # Place the monsters in the Generated room.
        place_entities(new_room, dungeon, engine.game_world.current_floor)
        dungeon.tiles[center_of_last_room] = tile_types.up_stairs
        dungeon.downstairs_location = center_of_last_room
        # Append the new room to the list.
        rooms.append(new_room)
    return dungeon
