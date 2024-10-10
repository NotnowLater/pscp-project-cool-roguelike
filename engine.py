""" The Game Engine itself"""

from __future__ import annotations
from typing import  TYPE_CHECKING

from tcod.console import Console

from render_functions import render_progress_bars, render_names_at_mouse_location
from message_log import MessageLog

import exceptions

from tcod.map import compute_fov

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap

class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.player = player
        self.mouse_location = (0, 0)

    def handle_enemy_turn(self):
        """ Handle All the enemies turn action """
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    # Ignore ai that perform the Impossible action
                    pass
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

    def render(self, console: Console) -> None:
        """ Render the game """
        self.game_map.render(console)

        # Render The player hp
        # console.print(x=1, y=61, string=f"HP {self.player.fighter.hp}/{self.player.fighter.max_hp}")
        render_progress_bars(console=console, current=self.player.fighter.hp, max=self.player.fighter.max_hp, total_width=20)
        self.message_log.render(console=console, x=35, y=46, width=60, height=8)
        render_names_at_mouse_location(console=console, x=1, y=48, engine=self)

