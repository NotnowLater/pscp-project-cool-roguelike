from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import colors
import components.ai_component
from components.base_component import BaseComponent
import components.inventory
from exceptions import Impossible
from input_handlers import (
    ActionOrHandler,
    AreaRangedAttackHandler,
    SingleRangedAttackHandler,
)

if TYPE_CHECKING:
    from entity import Actor, Item

class Consumable(BaseComponent):
    parent : Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action : actions.ItemAction) -> None:
        """
        Invoke this items ability.
        "action" is the context for this activation.
        """
        raise NotImplementedError()
    
    def consume(self) -> None:
        """ Remove the consumed(Activated) item from the inventory that contain the item. """
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)

class FlashConsumable(Consumable):
    def __init__(self, number_of_turns: int, radius: int):
        self.number_of_turns = number_of_turns
        self.radius = radius

    def get_action(self, consumer: Actor) -> AreaRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", colors.needs_target
        )
        return AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
            color=colors.white,
        )
 
    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")

        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"The {actor.name} is blinded by the flash and stumbles around!",
                    colors.status_effect_applied,
                )
                actor.ai = components.ai_component.BlindedEnemy(
                    entity=actor, previous_ai=actor.ai, turns_remaining=self.number_of_turns,
                )
                targets_hit = True

        if not targets_hit:
            raise Impossible("There are no targets in the radius.")
        self.consume()

class ExplosiveConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> AreaRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", colors.needs_target
        )
        return AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
            color=colors.red,
        )

    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")

        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"The {actor.name} is caught in the explosion, taking {self.damage} damage!"
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise Impossible("There are no targets in the radius.")
        self.consume()

class HealingConsumable(Consumable):
    def __init__(self, amount : int):
        self.amount = amount

    def activate(self, action : actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal_self(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",colors.health_recovered,)
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")

class AmmoConsumable(Consumable):
    def __init__(self, amount : int):
        self.amount = amount

    def activate(self, action : actions.ItemAction) -> None:
        consumer = action.entity
        consumer.fighter.ammo += self.amount

        self.engine.message_log.add_message(f"You open the {self.parent.name}, and got {self.amount} Ammo!",colors.health_recovered,)
        self.consume()
    