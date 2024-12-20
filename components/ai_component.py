""" Basic AI Component to control the entity. """

from __future__ import annotations

import random
from typing import List, Optional, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction, RangedAttackAction


if TYPE_CHECKING:
   from entity import Actor

class BaseAI(Action):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()
    
    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """ Compute and return a path to destination. Will Return an empty list if can't compute the path. """
        # Get the walkable array
        cost = np.array(self.entity.game_map.tiles["walkable"], dtype=np.int8)
        for entity in self.entity.game_map.entities:
            # Check the enitiy that blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add the cost of the blocked position
                # A lower number will make the enemies crowd together
                # A higher number will make the enemies try to surround the play
                cost[entity.x, entity.y] += 10
            # Create a graph from the cost array and pass that graph to a new pathfinder.
            graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
            pathfinder = tcod.path.Pathfinder(graph)
            # Add start position
            pathfinder.add_root((self.entity.x, self.entity.y))
            # Compute the path and remove the starting position.
            path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()
            return [(index[0], index[1]) for index in path]

class BlindedEnemy(BaseAI):
    """
    A blinded enemy will stumble around aimlessly for a given number of turns, then revert back to its previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(
        self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int
    ):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} can see again and regains its senses."
            )
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction due to blindness
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self.turns_remaining -= 1

            # The blinded actor will either try to move or attack in the chosen random direction.
            # It may bump into walls or miss an attack due to blindness.
            return BumpAction(self.entity, direction_x, direction_y,).perform()

class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))
        # If close enough to player, Attack the player.
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()
            self.path = self.get_path_to(target.x, target.y)
        # If Isn't close enough to player, move to player.
        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()
        # Wait if can't find a path to player
        return WaitAction(self.entity).perform()
    
class HostileRangedEnemy(BaseAI):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))
        # If the player can see this entity thats mean there is a clear los to player, so shoot at the player.
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            # Shoot if actually have ammo, otherwise just melee attack the enemy.
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()
            elif distance > 4 or not self.entity.fighter.ammo:
                self.path = self.get_path_to(target.x, target.y) 
            elif self.entity.fighter.ammo >= self.entity.fighter.ranged_attack_shot:
                return RangedAttackAction(self.entity, target_xy=(target.x, target.y)).perform()
            # self.path = self.get_path_to(target.x, target.y)
        # If Isn't close enough to player, move to player.
        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y,).perform()
        # Wait if can't find a path to player
        return WaitAction(self.entity).perform()

class TurretEnemy(BaseAI):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        # If the player can see this entity thats mean there is a clear los to player, so shoot at the player.
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            # Shoot if actually have ammo, otherwise just melee attack the enemy. 
            if self.entity.fighter.ammo >= self.entity.fighter.ranged_attack_shot:
                return RangedAttackAction(self.entity, target_xy=(target.x, target.y)).perform()
        return

class StaticEnemy(BaseAI):
    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []
    def perform(self) -> None:
        pass
