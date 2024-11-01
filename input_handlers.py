""" Handle all the input """

from __future__ import annotations

import os

from typing import Callable, Optional, Tuple, TYPE_CHECKING, Union

import tcod.event

from actions import Action, BumpAction, WaitAction, PickUpAction, DropItemAction, TakeStairsAction, EquipAction, RangedAttackAction
import components.item_pic 
import colors
import exceptions

from tcod import libtcodpy

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    # Numpad.
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_9: (1, -1),
    tcod.event.KeySym.KP_3: (1, 1),
}
WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
}

CONFIRM_KEYS = {
    tcod.event.KeySym.RETURN,
    tcod.event.KeySym.KP_ENTER,
}

CURSOR_Y_KEYS = {
   tcod.event.KeySym.UP: -1,
   tcod.event.KeySym.DOWN: 1,
   tcod.event.KeySym.PAGEUP: -10,
   tcod.event.KeySym.PAGEDOWN: 10,
}

RANGED_ATTACK_KEYS = {
    tcod.event.KeySym.f,
}

ActionOrHandler = Union[Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""

class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, console: tcod.console.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

class PopupMessage(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler: BaseEventHandler, text: str):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(console)
        console.tiles_rgb["fg"] //= 8
        console.tiles_rgb["bg"] //= 8

        console.print(
            console.width // 2,
            console.height // 2,
            self.text,
            fg=colors.white,
            bg=colors.black,
            alignment=tcod.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        """Any key returns to the parent handler."""
        return self.parent

class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine
    
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle events for input handlers with an engine."""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not self.engine.player.alive:
                # The player was killed sometime during or after the action.
                return GameOverEventHandler(self.engine)
            elif self.engine.player.level.requires_level_up:
                return LevelUpEventHandler(self.engine)
            return MainGameEventHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action: Optional[Action]) -> bool:
        """
        Handle actions returned from event methods.
        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], colors.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handle_enemy_turn()

        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event : tcod.event.MouseMotion) -> None:
        if self.engine.game_map.is_in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, console : tcod.console.Console):
        """ Tell the engine to call its render function (render the game). """
        self.engine.render(console=console)

class AskUserEventHandler(EventHandler):
    """ Handles user input for actions which require special input."""

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
       """By default any key exits this input handler."""
       if event.sym in {  # Ignore modifier keys.
           tcod.event.KeySym.LSHIFT,
           tcod.event.KeySym.RSHIFT,
           tcod.event.KeySym.LCTRL,
           tcod.event.KeySym.RCTRL,
           tcod.event.KeySym.LALT,
           tcod.event.KeySym.RALT,
       }:
           return None
       return self.on_exit()

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOrHandler]:
       """By default any mouse click exits this input handler."""
       return self.on_exit()

    def on_exit(self) -> Optional[ActionOrHandler]:
       """Called when the user is trying to exit or cancel an action.

       By default this returns to the main event handler.
       """
       return MainGameEventHandler(self.engine)

class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "Character Information"

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=7,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(
            x=x + 1, y=y + 1, string=f"Level: {self.engine.player.level.current_level}"
        )
        console.print(
            x=x + 1, y=y + 2, string=f"XP: {self.engine.player.level.current_xp}"
        )
        console.print(
            x=x + 1,
            y=y + 3,
            string=f"XP for next Level: {self.engine.player.level.experience_to_next_level}",
        )

        console.print(
            x=x + 1, y=y + 4, string=f"Strength: {self.engine.player.fighter.strength}"
        )
        console.print(
            x=x + 1, y=y + 5, string=f"Agility: {self.engine.player.fighter.agility}"
        )

class LevelUpEventHandler(AskUserEventHandler):
    TITLE = "Level Up"

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        console.draw_frame(
            x=x,
            y=0,
            width=35,
            height=8,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=1, string="Congratulations! You level up!")
        console.print(x=x + 1, y=2, string="Select an attribute to increase.")

        console.print(
            x=x + 2,
            y=3,
            string=f"[+{int(self.engine.player.fighter.max_hp / 5) + 2} HP, from {self.engine.player.fighter.max_hp}]",
            fg=colors.health_recovered
        )
        console.print(
            x=x + 1,
            y=4,
            string=f"A] STR [+2 STR, from {self.engine.player.fighter.strength}]",
        )
        console.print(
            x=x + 1,
            y=5,
            string=f"B] AGI [+2 AGI, from {self.engine.player.fighter.agility}]",
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.KeySym.a

        if 0 <= index <= 1:
            if index == 0:
                player.level.increase_max_hp(int(player.fighter.max_hp / 5) + 2)
                player.level.increase_attack(2)
            elif index == 1:
                player.level.increase_max_hp(int(player.fighter.max_hp / 5) + 2)
                player.level.increase_dv(2)
        else:
            self.engine.message_log.add_message("Invalid entry.", colors.invalid)

            return None

        return super().ev_keydown(event)

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOrHandler]:
        """
        Don't allow the player to click to exit the menu, like normal.
        """
        return None


class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: Engine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y

    def on_render(self, console: tcod.console.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.rgb["bg"][x, y] = colors.white
        console.rgb["fg"][x, y] = colors.black

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """Check for key movement or confirmation keys."""
        key = event.sym
        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y
            return None
        elif key == tcod.event.KeySym.w:
            nearest_enemy_pos = self.engine.game_map.get_nearest_enemy_pos(self.engine.player.x,self.engine.player.x)
            if nearest_enemy_pos:
                return self.on_index_selected(nearest_enemy_pos[0],nearest_enemy_pos[1])
            else:
                self.engine.message_log.add_message("No enemies in the area.", colors.impossible)
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOrHandler]:
        """Left click confirms a selection."""
        if self.engine.game_map.is_in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        """Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def on_index_selected(self, x: int, y: int) -> MainGameEventHandler:
        """Return to main handler."""
        return MainGameEventHandler(self.engine)

class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(self, engine: Engine, callback: Callable[[Tuple[int, int]], Optional[Action]]):
        super().__init__(engine)

        self.callback = callback
    
    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))

class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optional[Action]],
        color: tuple,
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback
        self.color = color
        print(callback)

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=self.color,
            clear=False,
        )

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        return self.callback((x, y))

class MainGameEventHandler(EventHandler):

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        # Hold action subclass
        action: Optional[Action] = None
        # Hold input key
        key = event.sym
        modifier = event.mod

        player = self.engine.player

        if key == tcod.event.KeySym.PERIOD and modifier & (
            tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT
        ):
            return TakeStairsAction(player)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)

        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.KeySym.ESCAPE:
            raise SystemExit()

        elif key == tcod.event.KeySym.m:
            return MessageLogHistoryViewer(self.engine)
        elif key == tcod.event.KeySym.g:
            action = PickUpAction(player)
        elif key == tcod.event.KeySym.i:
            return InventoryActivateHandler(self.engine)
        elif key == tcod.event.KeySym.d:
            return InventoryDropHandler(self.engine)
        elif key == tcod.event.KeySym.c:
            return CharacterScreenEventHandler(self.engine)
        elif key == tcod.event.KeySym.l:
            return LookHandler(self.engine)
        elif key == tcod.event.KeySym.h:
            for item in self.engine.player.inventory.items:
                if item.name == "Nano patch":
                    try:
                        item.consumable.activate(Action(self.engine.player))
                    except exceptions.Impossible as exc:
                        self.engine.message_log.add_message(exc.args[0], colors.impossible)
                    return
            self.engine.message_log.add_message("You don't have any Nano patches.", colors.impossible)
        elif key in RANGED_ATTACK_KEYS:
            if player.fighter.can_ranged_attack:
                return SingleRangedAttackHandler(self.engine, lambda xy:RangedAttackAction(player, xy))
        
        # No valid key was pressed
        return action

class GameOverEventHandler(EventHandler):
    def on_quit(self) -> None:
        """Handle exiting out of a finished game."""
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")  # Deletes the active save file.
        raise exceptions.QuitWithoutSaving()  # Avoid saving a finished game.

    def ev_quit(self, event: tcod.event.Quit) -> None:
        self.on_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.KeySym.ESCAPE:
            self.on_quit()
    
class MessageLogHistoryViewer(EventHandler):
    """ Print the message log history on a larger window which can be navigated. """
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.
        log_console = tcod.console.Console(console.width - 6, console.height - 6)
        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(0, 0, log_console.width, 1, "┤Message history├", alignment=libtcodpy.CENTER)
        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            log_console, 
            1, 
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == tcod.event.KeySym.HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.KeySym.END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            return MainGameEventHandler(self.engine)
        return None

def print_center_text(log_console, text, console_width, console_height, x_offset):
    lines = text.splitlines()
    num_lines = len(lines)
    # Calculate the vertical offset to center the text vertically
    vertical_offset = (console_height - num_lines) // 2
    for i, line in enumerate(lines):
        line_length = len(line)
        # Calculate leading spaces to center the line horizontally
        leading_spaces = (console_width - line_length) // 2
        # Print the line with adjusted x and y positions for centering
        log_console.print(leading_spaces + x_offset, vertical_offset + i, line)

item_description = {"Nano patch":"Recover 60 HP",
                    "Flash grenade":"Grants blindness to enemies in a\n\n      radius for 10 turns",
                    "Explosive grenade":"Deals 12 damage to all enemies\n\n      within a radius(including yourself)",
                    "Box of 20 Ammo":"Gain 20 ammo"
                    }

class InventoryEventHandler(AskUserEventHandler):
    """
    This handler lets the user select an item.
    What happens then depends on the subclass.
    """
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)
        self.cursor = 0
        self.scroll_offset = 0
        self.item_pic = components.item_pic.Item_pic
    TITLE = "Title Here"

    def on_render(self, console: tcod.console.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.
        number_of_items_in_inventory = len(self.engine.player.inventory.items)
        log_console = tcod.console.Console(console.width - 6, console.height - 6)

        max_visible_items = console.height - 6
        height = min(number_of_items_in_inventory + 2, max_visible_items)
        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(0, 0, log_console.width, 1, f"┤{self.TITLE}├", alignment=libtcodpy.CENTER)
        log_console.draw_frame(42, 2, log_console.width-44, log_console.height-4)
        # Render the message log using the cursor parameter.
        start_index = self.scroll_offset
        end_index = min(start_index + max_visible_items - 2, number_of_items_in_inventory)

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items[start_index:end_index]):
                is_equipped = self.engine.player.equipment.item_is_equipped(item)
                item_string = f"{item.name}"

                if is_equipped:
                    item_string = f" {item_string} (E)"

                if i + start_index != self.cursor:
                    item_string = f"- {item_string}"
                else:
                    item_string = f">  {item_string}  <"
                    print_center_text(log_console, self.item_pic.get(item.name, ""),72,30,30)
                    log_console.draw_frame(43, 30, log_console.width-46, 15, item.name)
                    if item.equippable is not None:
                        if item.equippable.equipment_type.value == 1:
                            if not item.equippable.ranged:
                                log_console.print(45, 32, f'"Melee ATK:"{item.equippable.attack_base+self.engine.player.fighter.attack_damage_bonus}-{((item.equippable.attack_roll+1)*(item.equippable.attack_die+1))+self.engine.player.fighter.attack_damage_bonus}')
                                log_console.print(46, 42, "[Melee Weapon]")
                            else:
                                log_console.print(45, 32, f'"Melee ATK:"{item.equippable.attack_base+self.engine.player.fighter.attack_damage_bonus}-{((item.equippable.attack_roll+1)*(item.equippable.attack_die+1))+self.engine.player.fighter.attack_damage_bonus}')
                                log_console.print(45, 34, f'"Range ATK:"{item.equippable.ranged_attack_base+self.engine.player.fighter.attack_damage_bonus}-{((item.equippable.ranged_attack_roll)*(item.equippable.ranged_attack_die))+self.engine.player.fighter.attack_damage_bonus}')
                                log_console.print(46, 42, "[Range Weapon]")
                        else:
                            log_console.print(45, 32, f'"DEF:+"{item.equippable.defense}')
                            log_console.print(45, 34, f'"AGI:+"{item.equippable.dv_bonus}')
                            log_console.print(46, 42, "[Armor]")
                    else:
                        log_console.print(45, 32, f'"USE:"{item_description[item.name]}')
                        log_console.print(46, 42, "[Consumable]")
                    log_console.print(75, 42, f'"weight:"{item.weight}')
                log_console.print(2, i + 1, item_string)
        else:
            log_console.print(1, 1, "(Empty)")
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        max_visible_items = 48
        number_of_items_in_inventory = len(self.engine.player.inventory.items)
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = number_of_items_in_inventory - 1
            elif adjust > 0 and self.cursor == number_of_items_in_inventory - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the Inventory.
                self.cursor = max(0, min(self.cursor + adjust, number_of_items_in_inventory - 1))
            if self.cursor < self.scroll_offset:
                self.scroll_offset = self.cursor
            elif self.cursor >= self.scroll_offset + max_visible_items - 2:
                self.scroll_offset = self.cursor - (max_visible_items - 3)
        elif event.sym == tcod.event.KeySym.HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.KeySym.END:
            self.cursor = number_of_items_in_inventory - 1  # Move directly to the last message.
        
        elif event.sym == tcod.event.KeySym.RETURN:
            if 0 <= self.cursor < number_of_items_in_inventory:
                selected_item = self.engine.player.inventory.items[self.cursor]
                return self.on_item_selected(selected_item)
        else:
            return MainGameEventHandler(self.engine)

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
       """Called when the user selects a valid item."""
       raise NotImplementedError()
   
class InventoryActivateHandler(InventoryEventHandler):
   """Handle using an inventory item."""

   TITLE = "Select an item to use"

   def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        if item.consumable:
            # Return the action for the selected item.
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return EquipAction(self.engine.player, item)
        else:
            return None


class InventoryDropHandler(InventoryEventHandler):
   """Handle dropping an inventory item."""

   TITLE = "Select an item to drop"

   def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
       """Drop this item."""
       return DropItemAction(self.engine.player, item)
