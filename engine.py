""" The Game Engine itself"""

from __future__ import annotations
from typing import  TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console

from input_handlers import EventHandler

from tcod.map import compute_fov
if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap
class Engine:
    def __init__(self, player: Entity):
        self.event_handler = EventHandler(self)
        self.player = player

    def handle_enemy_turn(self):
        """ Handle All the enemies turn action """
        for entity in self.game_map.entities - {self.player}:
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

        context.present(console)

        console.clear()

