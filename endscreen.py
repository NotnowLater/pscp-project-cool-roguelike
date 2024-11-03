""" The Game End Screen """
from __future__ import annotations

from typing import Optional

import colors

import tcod
import libtcodpy

import input_handlers
import setup_game


# Load the background image and remove the alpha channel.
background_image = tcod.image.load("end_background.png")[:, :, :3]

class EndScreen(input_handlers.BaseEventHandler):

    pmax_hp :int
    pstr :int
    pagi :int
    pxp :int
    plv :int

    def __init__(self, pmax: int = 0, pstr: int = 0, pagi: int = 0, pxp: int = 0, plv: int = 0) -> None:
        super().__init__()
        self.pmax_hp = pmax
        self.pstr = pstr
        self.pagi = pagi
        self.pxp = pxp
        self.plv = plv

    def on_render(self, console: tcod.console.Console) -> None:
        console.draw_semigraphics(background_image, 0, 0)
        console.print(
            console.width // 2,
            8,
            "The Station has been Destroyed",
            fg=colors.menu_text,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            10,
            "Mission Accomplished",
            fg=colors.menu_title,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            15,
            12,
            "END STATS",
            fg=colors.menu_text,
        )
        console.print(
            15,
            14,
            f"MAX Hp : {self.pmax_hp}",
            fg=colors.menu_text,
        )
        console.print(
            15,
            16,
            f"STR : {self.pstr}",
            fg=colors.menu_text,
        )
        console.print(
            15,
            18,
            f"AGI : {self.pagi}",
            fg=colors.menu_text,
        )
        console.print(
            15,
            20,
            f"TOTAL LEVEL : {self.plv}",
            fg=colors.menu_text,
        )
        console.print(
            15,
            22,
            f"TOTAL XP : {self.pxp}",
            fg=colors.menu_text,
        )
        console.print(
            console.width // 2,
            console.height - 10,
            "Press [ENTER] to return to main menu",
            fg=colors.menu_text,
            alignment=libtcodpy.CENTER,
        )
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym == tcod.event.KeySym.RETURN:
            return setup_game.MainMenu()