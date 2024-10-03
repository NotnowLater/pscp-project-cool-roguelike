""" Main Game Entry Point (PutTeamNameHere)"""

import tcod

from engine import Engine
import entity_factory
from dungen import generate_dungeon

import copy
import colors

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
    # player = Entity(40, 25, "@", (255, 255, 255))
    player = copy.deepcopy(entity_factory.player)
    game_engine = Engine(player=player)
    game_engine.game_map = generate_dungeon(
        max_rooms=max_rooms, 
        room_min_size=room_min_size, 
        room_max_size=room_max_size, 
        map_width=map_width,
        map_height=map_height, 
        engine=game_engine,
        max_monsters_per_room=max_monsters_per_room, 
    )
    game_engine.update_fov()
    # game_engine.message_log.add_message("Woo the message log freaking work!!!", stack=False)
    with tcod.context.new(
        width=1000,
        height=700,
        sdl_window_flags=tcod.context.SDL_WINDOW_RESIZABLE,
        tileset=tileset,
        title="RogueLike@Home",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        # main game loop here
        while True:
            root_console.clear()
            game_engine.event_handler.on_render(console=root_console)
            context.present(root_console, integer_scaling=True)
            game_engine.event_handler.handle_events(context)

if __name__ == "__main__":
    main()