""" Handle all the input """

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    # Numpad.
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_9: (1, -1),
    tcod.event.KeySym.KP_3: (1, 1),
}
WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
}

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

class MainGameEventHandler(EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turn()
            # Update the FOV before player next action.
            self.engine.update_fov()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        # Hold action subclass
        action: Optional[Action] = None
        # Hold input key
        key = event.sym
        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)

        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(player)

        # No valid key was pressed
        return action
    
class GameOverEventHandler(EventHandler):
    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction(self.engine.player)

        # No valid key was pressed
        return action