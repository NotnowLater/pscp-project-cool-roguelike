""" Define And Handle All the game action """

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        Perform this action with the objects needed to determine its scope.
        -engine is the scope this action is being performed in.
        -entity is the object performing the action.
        -This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        """ Perform Game Escape(Exit) Action"""
        raise SystemExit()

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
    
    def perform(self, engine: Engine, entity: Entity) -> None:
        """ Perform the Movement Action"""
        dest_x, dest_y = entity.x + self.dx, entity.y + self.dy
        if not engine.game_map.is_in_bounds(x=dest_x, y=dest_y):
            return # Destination is out of bounds, don't move.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination blocked, also don't move.
        entity.move(self.dx, self.dy)
        