""" Game Utility Functions """

import random

def roll_dice(dcount: int, dside: int, dplus) -> int:
    """ Return a rolled number from given dice parameters. """
    total = dplus
    for i in range(dcount):
        total +=random.randint(0, dside)
    return total

def hit_check(t_ac: int, p_tohit: int) -> bool:
    """ Return True if the will attack hit the target. """
    return roll_dice(1, 20, p_tohit) >= t_ac