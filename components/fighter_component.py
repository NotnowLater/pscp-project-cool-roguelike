""" A Figther Component class to make Entity able to Fight. """

from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from render_order import RenderOrder
import audiobrain

import colors

if TYPE_CHECKING:
   from entity import Actor

class Fighter(BaseComponent):
    """ A Figther Component class to make Entity able to Fight. """
    parent : Actor  # The parent entity that this component is attacth to.

    def __init__(self, hp: int, strength: int, agility: int, ammo: int):
        self.max_hp = hp
        self._hp = hp
        self.strength = strength
        self.agility = agility
        self._ammo = ammo

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
        new_hp = min(self.hp + amount, self.max_hp)
        
        recovered = new_hp - self.hp
        self.hp = new_hp
        return recovered

    def take_damage(self, amount : int) -> None:
        self.hp -= amount

    def get_stat_mods(self, stat: int) -> int:
        """ return the stats modifiler of the given stats value"""
        return int((stat - 10) / 2)

    @property
    def attack_damage_bonus(self) -> int:
        return self.get_stat_mods(self.strength) + self.equipment_attack_base

    @property
    def tohit(self) -> int:
        return self.get_stat_mods(self.strength) + self.equipment_tohit

    @property
    def dv(self) -> int:
        return 3 + self.get_stat_mods(self.agility) + self.dv_bonus

    @property
    def attack_die(self) -> int:
        return self.equipment_attack_die + 1

    @property
    def attack_roll(self) -> int:
        return self.equipment_attack_roll + 1

    @property
    def dv_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.dv_bonus
        else:
            return 0

    @property
    def equipment_tohit(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.tohit
        else:
            return 0

    @property
    def equipment_attack_die(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.attack_die
        else:
            return 0

    @property
    def equipment_attack_roll(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.attack_roll
        else:
            return 0
        
    @property
    def equipment_attack_base(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.attack_base
        else:
            return 0
        
    @property
    def can_ranged_attack(self):
        if self.parent.equipment:
            return self.parent.equipment.ranged
        else:
            return False

    @property
    def ranged_attack_die(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.ranged_attack_die
        else:
            return 0

    @property
    def ranged_attack_roll(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.ranged_attack_roll
        else:
            return 0

    @property
    def ranged_attack_base(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.ranged_attack_base
        else:
            return 0

    @property
    def ranged_tohit(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.ranged_tohit
        else:
            return 0

    @property
    def ammo(self) -> int:
            return self._ammo

    @ammo.setter
    def ammo(self, val: int) -> int:
            self._ammo = val

    @property
    def ranged_attack_shot(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.ranged_attack_shot
        else:
            return 0
        
    @property
    def equip_attack_snd_id(self) -> str:
        return self.parent.equipment.attack_snd_id
    def die(self) -> None:
        if self.engine.player is self.parent:
           death_message = "You died!"
           death_msg_color = colors.player_die
           audiobrain.game_over.play()
        else:
            if self.parent.name == "Item box":
                death_message = f"{self.parent.name} is destroyed!"
                death_msg_color = colors.enemy_die
                from dungen import item_box_drop_item
                item_box_drop_item(self.parent, self.engine.game_map, self.parent.fighter.ammo)
                self.engine.game_map.entities.remove(self.parent)
                self.engine.message_log.add_message(death_message, death_msg_color)
                return
            elif self.parent.name == "Table":
                death_message = f"{self.parent.name} is destroyed!"
                death_msg_color = colors.enemy_die
                self.engine.game_map.entities.remove(self.parent)
                self.engine.message_log.add_message(death_message, death_msg_color)
            else:
                death_message = f"{self.parent.name} is dead!"
                if self.parent.equipment:
                    from dungen import entity_drop_item
                    entity_drop_item(self.parent, self.engine.game_map, self.parent.equipment,self.parent.item_drop_chance)
                death_msg_color = colors.enemy_die
        if not (self.parent.x,self.parent.y) in [self.engine.game_map.upstairs_location,self.engine.game_map.endswitch_location]:
            self.parent.char = "%"
            self.parent.color = (191, 0, 0) 
        else:
            self.parent.char = ""
        self.parent.render_order = RenderOrder.CORPSE
        self.parent.name = f"Corpse of {self.parent.name}"
        self.parent.ai = None
        self.parent.blocks_movement = False
        self.engine.message_log.add_message(death_message, death_msg_color)
        self.engine.player.level.add_xp(self.parent.level.xp_given)
