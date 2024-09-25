""" Main Game Entry Point """

import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler

def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x, player_y = 40, 25

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

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
            root_console.print(x=player_x, y=player_y, string="@")
            context.present(root_console)
            root_console.clear()
            # main events
            for event in tcod.event.wait():
                action = event_handler.dispatch(event)
                if action is None:
                    continue
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()