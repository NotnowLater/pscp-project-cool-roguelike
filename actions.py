""" Define And Handle All the game action """

from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

# from engine import Engine
# from entity import Entity

import util
import colors

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor

class Action:
    def __init__(self, entity: Actor) -> None:
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
    def __init__(self, entity: Actor, dx: int, dy: int) -> None:
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

    @property
    def action_target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self) -> None:
        """ Perform Game Escape(Exit) Action. """
        raise SystemExit()

class MeleeAction(ActionWithDirection):
    """" Perform Melee(attack) action to an entity in that direction."""
    def perform(self) -> None:
        target = self.action_target_actor
        # Check if has target to attack
        if not target:
            return
        # Attack hit check.
        if not util.hit_check(target.fighter.dv, 0):
            self.engine.message_log.add_message(f"{self.entity.name.capitalize()} Attack the {target.name} but missed.", fg=colors.enemy_atk)
            return
        dmg = util.roll_dice(1, self.entity.fighter.attack, 0)

        if self.entity is self.engine.player:
            attack_color = colors.player_atk
        else:
            attack_color = colors.enemy_atk
        self.engine.message_log.add_message(f"{self.entity.name.capitalize()} Attacks {target.name} for {dmg} hit points.", fg=attack_color)
        target.fighter.hp -= dmg

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
        if self.action_target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
    
class WaitAction(Action):
    """ Just Wait. """
    def perform(self) -> None:
        pass