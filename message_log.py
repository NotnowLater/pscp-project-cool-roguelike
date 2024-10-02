""" Define The Player Message log """

from typing import List ,Reversible, Tuple
import textwrap

import tcod
import colors

class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]) -> None:
        self.text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        """ The full text of this message (including the count in some message). """
        if self.count > 1:
            return f"{self.text} x{self.count}"
        return self.text
    
class MessageLog:
    def __init__(self) -> None:
        self.messages : List[Message] = []

    def add_message(
            self,
            text : str,
            fg : Tuple[int, int, int] = colors.white,
            *, stack : bool = True
        ) -> None:
        """ 
        Add the message to this log.
        text is the message text.
        fg is text color.
        if stack is True, this message will stack with the previous message of the same text.
        """
        if stack and self.messages and text == self.messages[-1].text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text=text, fg=fg))

    def render(
            self,
            console : tcod.console.Console,
            x : int,
            y : int,
            width : int,
            height: int,
        ) -> None:
        """ render this message log at the given position at the given size. """
        self.render_messages(console=console, x=x, y=y, width=width, height=height, messages=self.messages)

    @staticmethod
    def render_messages(
        console : tcod.console.Console,
        x : int,
        y : int,
        width : int,
        height : int,
        messages : Reversible[Message],
    ) -> None:
        """
        Render the messages provided.
        The "messages" are rendered starting at the last message and working backwards to the first message.
        """
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # No more space to print messages.