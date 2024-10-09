""" Main Game Entry Point (PutTeamNameHere)"""

import tcod

from engine import Engine
import entity_factory
from dungen import generate_dungeon

import copy
import traceback
import colors

def main() -> None:
    screen_width = 100
    screen_height = 70

    window_width = 1000
    window_height = 700

    max_monsters_per_room = 4
    max_items_per_room = 2

    map_width, map_height = 100, 60
    room_max_size = 10
    room_min_size = 5
    max_rooms = 30
    tileset = tcod.tileset.load_tilesheet(
        "newtile16x16.png", 16, 16, tcod.tileset.CHARMAP_CP437
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
        max_items_per_room=max_items_per_room
    )
    game_engine.update_fov()
    game_engine.message_log.add_message("Welcome to the dungeon", stack=False, fg=colors.welcome_text)
    with tcod.context.new(
        width=window_width,
        height=window_height,
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
            try:
                for event in tcod.event.wait():
                    context.convert_event(event=event)
                    game_engine.event_handler.handle_events(event)
            except Exception:   # Handle in Game exceptions here.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                game_engine.message_log.add_message(traceback.format_exc(), colors.error)
        
if __name__ == "__main__":
    main()