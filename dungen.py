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
    (1, 1),
    (6, 2),
]

#(Floor, Max Item)
max_items_for_floor_by_floor = [
    (1, 3),
    (3, 4),
    (4, 5),
    (6, 6),
    (7, 7), 
    (10, 10),
]

#(Floor, Max Monsters)
max_monsters_by_floor = [
    (1, 3),
    (4, 4),
    (6, 5),
]

#(Floor, Max special rooms)
max_special_rooms_by_floor = [
    (1, 3),
    (4, 4),
    (7, 5),
    (9, 6),
    (14, 7),
]

#(Floor, Chance)
special_room_appear_chance: Dict = {
    0: 0.05,
    2: 0.09,
    3: 0.14,
    4: 0.24,
    5: 0.3,
    7: 0.34,
    9: 0.38,
}

#(Floor, Max Monsters)
special_room_type_chance: Dict[int, List[Tuple[int, int]]] = {
    0: [(0, 5),(1, 5)],
    2: [(2, 5),(12, 3),(6, 2),(16, 2)],
    3: [(3, 4),(4, 5),(8, 3),(9, 1),(11, 2),(13, 3),(15, 2),(10, 2),(7, 3),(18,2)],
    4: [(1, 0),(3, 0),(4, 0),(6, 0),(7, 0),(10, 0),(15, 0),(12, 0),(16, 0),(2, 0),(0, 0),
        (5, 3),(14, 4)],
    5: [(17,2),(19,3),(20,1),(21,3),(22,1)],
    6: [(5, 0),(11, 0),(13, 0),(14, 0),(18, 0)]
}

#(Type, [Min_x ,Max_x, Min_y, Max_y, [(Entity,(pos_x,pos_y))]]])
#        --------Room size----------  -----Entity in Room-----
special_room_attribute: Dict = {
    0: (7,7,7,7,[(entity_factory.item_box,(3,3))],[]),
    1: (10,10,10,10,[(entity_factory.table,(3,3)),(entity_factory.table,(7,3)),
                     (entity_factory.table,(3,6)),(entity_factory.table,(7,6)),
                     (entity_factory.janitor,(3,4)),(entity_factory.janitor,(7,4)),
                     (entity_factory.janitor,(3,7)),(entity_factory.janitor,(7,7))],[]),
    2: (10,10,10,10,[(entity_factory.table,(8,2)),(entity_factory.table,(2,8)),
                     (entity_factory.item_box,(2,2)),(entity_factory.security,(5,5)),
                     (entity_factory.janitor,(8,1)),],[]),
    3: (10,10,10,10,[(entity_factory.item_box,(5,5)),(entity_factory.security,(4,4)),
                     (entity_factory.security,(6,4)),(entity_factory.security,(4,6)),(entity_factory.bandage,(5,2)),
                     (entity_factory.security,(6,6))],[(tile_types.wall2,(2,2)),
                     (tile_types.wall2,(8,2)),(tile_types.wall2,(2,8)),(tile_types.wall2,(8,8))]),
    4: (10,10,10,10,[(entity_factory.security,(5,5)),(entity_factory.bandage,(random.randint(3,8),random.randint(3,4)))],
                     [(tile_types.wall2,(2,2)),(tile_types.wall2,(8,2)),(tile_types.wall2,(2,8)),(tile_types.wall2,(8,8))]),
    5: (10,10,10,10,[(entity_factory.sword,(5,5))],[(tile_types.wall2,(2,2)),
                    (tile_types.wall2,(8,2)),(tile_types.wall2,(2,8)),(tile_types.wall2,(8,8))]),
    6: (10,10,10,10,[(entity_factory.item_box,(5,5)),(entity_factory.table,(4,4)),
                     (entity_factory.table,(6,4)),(entity_factory.table,(4,6)),
                     (entity_factory.table,(6,6)), (entity_factory.table,(4,5)),
                     (entity_factory.table,(6,5)), (entity_factory.table,(5,4)),
                     (entity_factory.table,(5,6))],[]),
    7: (10,10,10,10,[(entity_factory.janitor,(4,4)),(entity_factory.janitor,(5,4)),
                     (entity_factory.janitor,(6,4)),(entity_factory.janitor,(4,5)),
                     (entity_factory.janitor,(6,5)), (entity_factory.janitor,(4,6)),
                     (entity_factory.janitor,(5,6)), (entity_factory.janitor,(6,6)),
                     ],[(tile_types.wall2,(5,5))]),
    8: (10,10,10,10,[(entity_factory.item_box,(7,2)),(entity_factory.item_box,(8,2)),
                     (entity_factory.item_box,(7,3)),(entity_factory.item_box,(8,3)),
                     ],[(tile_types.wall2,(5,5))]),
    9: (10,10,10,10,[(entity_factory.item_box,(7,2)),(entity_factory.item_box,(8,2)),
                     (entity_factory.item_box,(7,3)),(entity_factory.item_box,(8,3)),
                     (entity_factory.item_box,(2,2)),(entity_factory.item_box,(3,2)),
                     (entity_factory.item_box,(2,3)),(entity_factory.item_box,(3,3)),
                     ],[(tile_types.wall2,(5,5))]),
    10: (10,10,10,10,[(entity_factory.security,(4,2)),(entity_factory.security,(6,2)),
                     (entity_factory.crew,(5,2)),(entity_factory.table,(4,3)),
                     (entity_factory.table,(5,3)), (entity_factory.table,(6,3)),
                     ],[(tile_types.wall2,(5,5))]),
    11: (10,10,10,10,[(entity_factory.item_box,(2,2)),(entity_factory.item_box,(8,2)),
                     (entity_factory.item_box,(2,8)),(entity_factory.item_box,(8,8)),
                     ],[(tile_types.wall2,(5,5))]),
    12: (10,10,10,10,[(entity_factory.crew,(3,3)),(entity_factory.crew,(7,7)),
                     ],[(tile_types.wall2,(5,5))]),
    13: (10,10,10,10,[(entity_factory.item_box,(3,5)),(entity_factory.table,(5,4)),
                      (entity_factory.table,(6,4)),(entity_factory.table,(6,5)),(entity_factory.bandage,(2,8))
                     ],[(tile_types.wall2,(5,5))]),
    14: (10,10,10,10,[(entity_factory.security,(8,2)),(entity_factory.security,(8,5)),
                      (entity_factory.security,(8,8)),
                     ],[(tile_types.wall2,(4,4)),(tile_types.wall2,(5,4)),(tile_types.wall2,(6,4)),
                        (tile_types.wall2,(4,5)),(tile_types.wall2,(6,5)),(tile_types.wall2,(4,6)),
                        (tile_types.wall2,(5,6)),(tile_types.wall2,(6,6))]),
    15: (10,10,10,10,[(entity_factory.security,(2,2)),(entity_factory.security,(5,8)),
                      (entity_factory.janitor,(8,2)),(entity_factory.item_box,(8,5))
                     ],[(tile_types.wall2,(4,4)),(tile_types.wall2,(5,4)),(tile_types.wall2,(6,4)),
                        (tile_types.wall2,(4,5)),(tile_types.wall2,(6,5)),(tile_types.wall2,(4,6)),
                        (tile_types.wall2,(5,6)),(tile_types.wall2,(6,6))]),
    16: (10,10,10,10,[(entity_factory.bandage,(5,1)),
                      (entity_factory.janitor,(8,2)),(entity_factory.item_box,(8,7))
                     ],[(tile_types.wall2,(4,4)),(tile_types.wall2,(5,4)),(tile_types.wall2,(6,4)),
                        (tile_types.wall2,(4,5)),(tile_types.wall2,(6,5)),(tile_types.wall2,(4,6)),
                        (tile_types.wall2,(5,6)),(tile_types.wall2,(6,6))]),
    17: (10,10,10,10,[(entity_factory.bandage,(8,2)),(entity_factory.ammo20,(2,8)),
                      (entity_factory.error_clone01,(8,5)),(entity_factory.error_clone01,(5,2)),(entity_factory.error_clone01,(2,5))
                     ],[(tile_types.wall2,(4,4)),(tile_types.wall2,(5,4)),(tile_types.wall2,(6,4)),
                        (tile_types.wall2,(4,5)),(tile_types.wall2,(6,5)),(tile_types.wall2,(4,6)),
                        (tile_types.wall2,(5,6)),(tile_types.wall2,(6,6))]),
    18: (10,10,10,10,[(entity_factory.bandage,(5,5)),(entity_factory.ammo20,(7,2))],[(tile_types.wall2,(2,2)),
                    (tile_types.wall2,(8,2)),(tile_types.wall2,(2,8)),(tile_types.wall2,(8,8))]),
    19: (10,10,10,10,[(entity_factory.item_box,(8,4)),(entity_factory.item_box,(8,6)),
                      (entity_factory.bandage,(8,5))
                     ],[(tile_types.wall2,(4,4)),(tile_types.wall2,(5,4)),(tile_types.wall2,(6,4)),
                        (tile_types.wall2,(4,5)),(tile_types.wall2,(6,5)),(tile_types.wall2,(4,6)),
                        (tile_types.wall2,(5,6)),(tile_types.wall2,(6,6))]),
    20: (10,10,10,10,[(entity_factory.ammo20,(1,1)),(entity_factory.ammo20,(9,9))],
                        [(tile_types.wall2,(4,4)),(tile_types.wall2,(5,4)),(tile_types.wall2,(6,4)),
                        (tile_types.wall2,(4,5)),(tile_types.wall2,(6,5)),(tile_types.wall2,(4,6)),
                        (tile_types.wall2,(5,6)),(tile_types.wall2,(6,6))]),
    21: (6,6,6,6,[(entity_factory.ammo20,(2,3)),(entity_factory.bandage,(4,3)),(entity_factory.item_box,(3,3))],[(tile_types.wall2,(2,2)),
                    (tile_types.wall2,(4,2)),(tile_types.wall2,(2,4)),(tile_types.wall2,(4,4))]),
    22: (6,6,6,6,[(entity_factory.ammo20,(3,3))],[(tile_types.wall2,(2,2)),
                    (tile_types.wall2,(4,2)),(tile_types.wall2,(2,4)),(tile_types.wall2,(4,4))]),
}

#(Type, Item in Box)
item_box_chance: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factory.bandage, 18), (entity_factory.ammo20, 13),
        (entity_factory.flash_grenade, 12),(entity_factory.explosive_grenade, 5),
        (entity_factory.sword, 4),(entity_factory.chain_mail, 4),
        (entity_factory.dagger, 20),(entity_factory.leather_armor, 15),(entity_factory.pistol, 9)],
    1: [(entity_factory.flash_grenade, 25), (entity_factory.sword, 10),
        (entity_factory.explosive_grenade, 5), (entity_factory.bandage, 20),
        (entity_factory.ammo20, 10)],
}

#(Floor, Item)
item_chance: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factory.bandage, 50)],
    2: [(entity_factory.flash_grenade, 10),(entity_factory.ammo20, 10)],
    3: [(entity_factory.ammo20, 23)],
    4: [(entity_factory.explosive_grenade, 10)],
    5: [(entity_factory.ammo20, 33)],
}

#(Floor, Enemy)
enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factory.janitor, 50),(entity_factory.crew, 1),(entity_factory.item_box, 1)],
    2: [(entity_factory.crew, 15)],
    3: [(entity_factory.security, 20),(entity_factory.item_box, 4)],
    4: [(entity_factory.crew, 20), (entity_factory.item_box, 5), (entity_factory.security_smg, 25),(entity_factory.janitor, 0)],
    5: [(entity_factory.combat_droid, 20),(entity_factory.security, 30), (entity_factory.security_smg, 30)],
    6: [(entity_factory.combat_droid, 32),(entity_factory.crew, 0)],
    #7 : New Item box
    8: [(entity_factory.error_clone01, 20),(entity_factory.error_clone02, 20)],
    9: [(entity_factory.marine_ba, 20),(entity_factory.marine_sa, 20)],
    10: [(entity_factory.marine_ap, 20),(entity_factory.marine_la, 20)],
    11: [(entity_factory.beam_turret, 20),(entity_factory.pulse_turret, 20)],
    12: [(entity_factory.human_kimera, 20)],
    13: [(entity_factory.material_kimera, 20)],
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

def get_chance(floor_number: int, chance_dict: dict) -> bool:
    chance = 0.0
    for floor, prob in chance_dict.items():
        if floor < floor_number:
            chance = prob
        else:
            break
    return random.random() < chance

ITEM_COUNT = 0
def place_entities(room : RectangularRoom, dungeon: GameMap, floor_number : int,) -> None:
    global ITEM_COUNT
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

    for entity in monsters:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        # Check if the entity is overlapping the existing entity first before placing it.
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn_copy(dungeon, x, y)
    
    max_item_for_floor = get_max_value_for_floor(max_items_for_floor_by_floor, floor_number)
    for entity in items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)
        # Check if the entity is overlapping the existing entity first before placing it.
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities) and ITEM_COUNT < max_item_for_floor:
            ITEM_COUNT += 1
            entity.spawn_copy(dungeon, x, y)

def place_entities_in_special_room(room: RectangularRoom, dungeon: GameMap, type: int) -> None:
    """spawn entites in special room"""
    for entity, (entity_x, entity_y) in special_room_attribute[type[0]][4]:
        if not any(entity.x == entity_x and entity.y == entity_y for entity in dungeon.entities):
            entity.spawn_copy(dungeon, room.x1 + entity_x, room.y1 + entity_y)
    for tile, (x,y) in special_room_attribute[type[0]][5]:
        dungeon.tiles[(room.x1 + x,room.y1 + y)] = tile

def generate_dungeon(
        max_rooms: int, room_min_size: int, room_max_size: int,
        map_width: int, map_height: int, engine: Engine,
    ) -> GameMap:
    """ Return The Generated Dungeon of given size. """
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms: List[RectangularRoom] = []
    center_of_last_room = (0, 0)
    current_floor = engine.game_world.current_floor
    max_sp_room = get_max_value_for_floor(max_special_rooms_by_floor,current_floor)
    sp_room_count = 0
    global ITEM_COUNT
    ITEM_COUNT = 0
    for r in range(max_rooms):
        #len(rooms) > 1 to fix that first and second rooms isn't special room
        special_room = get_chance(current_floor,special_room_appear_chance) and len(rooms) > 1 and sp_room_count < max_sp_room

        if not special_room:
            room_width = random.randint(room_min_size, room_max_size)
            room_height = random.randint(room_min_size, room_max_size)
        else:
            special_room_type = get_entities_at_random(special_room_type_chance, 1, current_floor)
            room_width = random.randint(special_room_attribute[special_room_type[0]][0], special_room_attribute[special_room_type[0]][1])
            room_height = random.randint(special_room_attribute[special_room_type[0]][2], special_room_attribute[special_room_type[0]][3])

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
                if dungeon.tiles[x, y] != tile_types.wall2:
                    dungeon.tiles[x, y] = tile_types.floor
            if not special_room:
                center_of_last_room = new_room.center

        # Place the monsters in the Generated room.
        if special_room:
            sp_room_count += 1
            place_entities_in_special_room(new_room, dungeon, special_room_type)
        else:
            place_entities(new_room, dungeon, current_floor)
        # Append the new room to the list.
        rooms.append(new_room)
    if current_floor != 20:
        dungeon.tiles[center_of_last_room] = tile_types.up_stairs
        dungeon.upstairs_location = center_of_last_room
    else:
        dungeon.tiles[center_of_last_room] = tile_types.end_switch
        dungeon.endswitch_location = center_of_last_room
    return dungeon
