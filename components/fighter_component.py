""" A Figther Component class to make Entity able to Fight. """

from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from render_order import RenderOrder

import colors

if TYPE_CHECKING:
   from entity import Actor

class Fighter(BaseComponent):
    """ A Figther Component class to make Entity able to Fight. """
    parent : Actor  # The parent entity that this component is attacth to.

    def __init__(self, hp: int, base_dv: int, base_attack: int):
        self.max_hp = hp
        self._hp = hp
        self.base_dv  = base_dv
        self.base_attack = base_attack

    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, val: int):
        self._hp = max(0, min(val, self.max_hp))
        if self._hp <= 0 and self.parent.ai:
            self.die()

    def heal_self(self, amount : int) -> int:
        if self.hp == self.max_hp:
            return 0
        # limit the healing to max hp.
        new_hp = max(self.hp + amount, self.max_hp)
        
        recovered = new_hp - self.hp
        self.hp = new_hp
        return recovered

    def take_damage(self, amount : int) -> None:
        self.hp -= amount

    @property
    def dv(self) -> int:
        return self.base_dv + self.dv_bonus

    @property
    def attack(self) -> int:
        return self.base_attack + self.attack_bonus

    @property
    def dv_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.dv_bonus
        else:
            return 0

    @property
    def attack_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.attack_bonus
        else:
            return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
           death_message = "You died!"
           death_msg_color = colors.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_msg_color = colors.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"Corspe of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_msg_color)
        self.engine.player.level.add_xp(self.parent.level.xp_given)
