""" Main Game Entry Point """

import tcod

from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap
from dungen import generate_dungeon

def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width, map_height = 80, 45
    room_max_size = 10
    room_min_size = 5
    max_rooms = 30
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()
    player = Entity(40, 25, "@", (255, 255, 255))
    npc = Entity(45, 15, "@", (0, 255, 255))
    entities = {player, npc}
    game_map = generate_dungeon(max_rooms, room_min_size, room_max_size, map_width, map_height, player)
    game_engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

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