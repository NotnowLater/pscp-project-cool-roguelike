""" The Game Engine itself"""

from typing import  Iterable, Any

from tcod.context import Context
from tcod.console import Console

from input_handlers import EventHandler
from game_map import GameMap
from tcod.map import compute_fov
from entity import Entity

class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap ,player: Entity):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turn(self):
        """ Handle All the enemies turn action """
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders about all the thing it could do it if can take a real turn.')

    def handle_events(self, events: Iterable[Any]) -> None:
        """ Handle All the Game Events """
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)
            self.handle_enemy_turn()
            # Update the FOV before the players next action.
            self.update_fov()

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

