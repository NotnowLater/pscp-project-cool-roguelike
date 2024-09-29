""" A Figther Component class to make Entity able to Fight. """

from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from render_order import RenderOrder
from input_handlers import GameOverEventHandler

if TYPE_CHECKING:
   from entity import Actor

class Fighter(BaseComponent):
    """ A Figther Component class to make Entity able to Fight. """
    entity: Actor

    def __init__(self, hp: int, dv: int, attack: int) -> None:
        self.max_hp = hp
        self._hp = hp
        self.dv = dv
        self.attack = attack

    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, val: int):
        self._hp = max(0, min(val, self.max_hp))
        if self._hp <= 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.entity:
           death_message = "You died!"
           self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.entity.name} is dead!"

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"Corspe of {self.entity.name}"
        self.entity.render_order = RenderOrder.CORPSE

        print(death_message)

