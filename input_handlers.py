""" Handle all the input """

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction

if TYPE_CHECKING:
    from engine import Engine

class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turn()
            # Update the FOV before player next action.
            self.engine.update_fov()


    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        # Hold action subclass
        action: Optional[Action] = None
        # Hold input key
        key = event.sym
        player = self.engine.player

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.KP_8:
            action = BumpAction(player, dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.KP_2:
            action = BumpAction(player, dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.KP_4:
            action = BumpAction(player, dx=-1, dy=0)
        elif key == tcod.event.KeySym.KP_1:
            action = BumpAction(player, dx=-1, dy=1)
        elif key == tcod.event.KeySym.KP_7:
            action = BumpAction(player, dx=-1, dy=-1)
        elif key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.KP_6:
            action = BumpAction(player, dx=1, dy=0)
        elif key == tcod.event.KeySym.KP_3:
            action = BumpAction(player, dx=1, dy=1)
        elif key == tcod.event.KeySym.KP_9:
            action = BumpAction(player, dx=1, dy=-1)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)

        # No valid key was pressed
        return action