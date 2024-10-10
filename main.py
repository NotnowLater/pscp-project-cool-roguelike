""" Main Game Entry Point (PutTeamNameHere)"""

import tcod

import exceptions
import input_handlers
import setup_game

import traceback
import colors

def main() -> None:
    screen_width = 96
    screen_height = 54

    window_width = 960
    window_height = 540

    tileset = tcod.tileset.load_tilesheet(
        "newtile16x16.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()
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
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), colors.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            # TODO: Add the save function here
            raise
        except BaseException:  # Save on any other unexpected exception.
            # TODO: Add the save function here
            raise
        
if __name__ == "__main__":
    main()