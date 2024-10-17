""" Define the inventory component for the player. """

from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int = 0, item: List[Item] = []):
        self._capacity = capacity
        self.items = item

    def drop(self, item: Item, ) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place_at(self.parent.x, self.parent.y, self.game_map)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")

    @property
    def capacity(self):
        """ Return totoal capacity of this inventory"""
        return self._capacity
    
    @capacity.setter
    def capacity(self, val: int):
        self._capacity = val

    @property
    def total_weight(self):
        """ Return the total weights of all item in this inventory"""
        total = 0
        for it in self.items:
            total += it.weight
        return total