""" Define And Handle All the game action """

from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

# from engine import Engine
# from entity import Entity

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """ Return the engine this action belongs to. """
        return self.entity.game_map.engine

    def perform(self) -> None:
        """
        Perform this action with the objects needed to determine its scope.
        -self.engine is the scope this action is being performed in.
        -self.entity is the object performing the action.
        -This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()
    
class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int) -> None:
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """ Return this action destination. """
        return self.entity.x + self.dx, self.entity.y + self.dy
    
    @property
    def action_blocking_entity(self) -> Optional[Entity]:
        """ Return the blocking entity at this action destination. """
        return self.engine.game_map.get_blocking_entity_at(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self) -> None:
        """ Perform Game Escape(Exit) Action. """
        raise SystemExit()

class MeleeAction(ActionWithDirection):
    """" Perform Melee(attack) action to an entity in that direction."""
    def perform(self) -> None:
        target = self.action_blocking_entity
        if not target:
            return
        print(f"You push the {target.name}, {target.name} seem to be annoyed by your action.")

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        """ Perform the Movement Action"""
        dest_x, dest_y = self.dest_xy
        if not self.engine.game_map.is_in_bounds(x=dest_x, y=dest_y):
            return # Destination is out of bounds, don't move.
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination blocked, also don't move.
        if self.engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            return
        self.entity.move(self.dx, self.dy)
        
class BumpAction(ActionWithDirection):
    """ An Action class to determine if the Action should be Melee or Movement Action """
    def perform(self) -> None:
        if self.action_blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
    