""" The Game Engine itself"""

from __future__ import annotations
from typing import  TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console

from input_handlers import MainGameEventHandler

from tcod.map import compute_fov

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler

class Engine:
    def __init__(self, player: Actor):
        self.event_handler = MainGameEventHandler(self)
        self.player = player

    def handle_enemy_turn(self):
        """ Handle All the enemies turn action """
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()
            else:
                print(f'The {entity.name} wonders about all the thing it could do it if can take a real turn.')

    def update_fov(self) -> None:
        """ Compute the visible area based on the players point of view. """
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If the tile is visible, add it to the "seen"
        self.game_map.seen |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        """ Render the game """
        self.game_map.render(console)

        # Render The player hp
        console.print(x=1, y=61, string=f"HP {self.player.fighter.hp}/{self.player.fighter.max_hp}")

        context.present(console)

        console.clear()

