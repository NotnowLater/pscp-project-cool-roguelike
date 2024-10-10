""" Defines all the game exceptions. """

class Impossible(Exception):
    """ 
    Exception that raised when the action is impossible to perform.
    The Reason is given as the exception message.
    """
    pass

class QuitWithoutSaving(SystemExit):
    """Can be raised to exit the game without automatically saving."""
    pass
