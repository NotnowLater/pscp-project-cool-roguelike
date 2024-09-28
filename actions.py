""" Define And Handle All the game action """

from __future__ import annotations
from typing import TYPE_CHECKING

# from engine import Engine
# from entity import Entity

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
    
class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int) -> None:
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        """ Perform Game Escape(Exit) Action"""
        raise SystemExit()

class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x, dest_y = entity.x + self.dx, entity.y + self.dy
        target = engine.game_map.get_blocking_entity_at(dest_x, dest_y)
        if not target:
            return
        print(f"You push the {target.name}, {target.name} seem to be annoyed by your action.")

class MovementAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        """ Perform the Movement Action"""
        dest_x, dest_y = entity.x + self.dx, entity.y + self.dy
        if not engine.game_map.is_in_bounds(x=dest_x, y=dest_y):
            return # Destination is out of bounds, don't move.
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination blocked, also don't move.
        if engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            return
        entity.move(self.dx, self.dy)
        
class BumpAction(ActionWithDirection):
    """ An Action class to determine if the Action should be Melee or Movement Action """
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x, dest_y = entity.x + self.dx, entity.y + self.dy
        if engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
    