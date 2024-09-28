""" Main Game Entry Point """

import tcod

from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap
import entity_factory
from dungen import generate_dungeon

import copy

def main() -> None:
    screen_width = 100
    screen_height = 70
    max_monsters_per_room = 2
    map_width, map_height = 100, 60
    room_max_size = 10
    room_min_size = 5
    max_rooms = 30
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()
    # player = Entity(40, 25, "@", (255, 255, 255))
    player = copy.deepcopy(entity_factory.player)
    game_map = generate_dungeon(
        max_rooms, room_min_size, room_max_size, map_width,
        map_height, player, max_monsters_per_room, 
    )
    game_engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Game nane here",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        # main game loop here
        while True:
            game_engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            game_engine.handle_events(events)


if __name__ == "__main__":
    main()