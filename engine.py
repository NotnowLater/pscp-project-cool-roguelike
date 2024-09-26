""" The Game Engine itself"""

from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap
from tcod.map import compute_fov

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap ,player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        """ Handle All the Game Events """
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)
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

        for entity in self.entities:
            # Only draw the entities that are in the FOV 
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()

