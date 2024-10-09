""" Define And Handle All the game action """

from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

# from engine import Engine
# from entity import Entity

from entity import Actor
import util
import colors
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor, Item

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

class ItemAction(Action):
    def __init__(self, entity : Actor, item : Item, target_xy: Optional[Tuple[int, int]] = None):
        super().__init__(entity=entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def action_target_actor(self) -> Optional[Actor]:
        """ Return the actor at this actions destination. """
        return self.engine.game_map.get_actor_at(*self.target_xy)
    
    def perform(self) -> None:
        """ Invoke the items ability, this action will be given to provide context. """
        self.item.consumable.activate(self)

class MeleeAction(ActionWithDirection):
    """" Perform Melee(attack) action to an entity in that direction."""
    def perform(self) -> None:
        target = self.action_target_actor
        # Check if has target to attack
        if not target:
            raise exceptions.Impossible("No target to attack.")
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
            # Destination is out of bounds, don't move.
            raise exceptions.Impossible("The Way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination blocked, also don't move.
            raise exceptions.Impossible("The Way is blocked.")
        if self.engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            # Destination blocked by an entity, also don't move.
            raise exceptions.Impossible("The Way is blocked.")
        self.entity.move(self.dx, self.dy)
        
class BumpAction(ActionWithDirection):
    """ An Action class to determine if the Action should be Melee or Movement Action """
    def perform(self) -> None:
        if self.action_target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
    
class PickUpAction(Action):
    """ Pickup an item and add it to the inventory if there is room for it. """
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)
    
    def perform(self) -> None:
        actor_x = self.entity.x
        actor_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_x == item.x and actor_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your Inventory is full.")
                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return
        
        raise exceptions.Impossible("There is nothing on the Ground here to pick up.")

class DropItemAction(ItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)

class WaitAction(Action):
    """ Just Wait. """
    def perform(self) -> None:
        pass