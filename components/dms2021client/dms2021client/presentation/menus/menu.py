""" Menu class module.
"""

from abc import ABC, abstractmethod
from typing import List

class Menu(ABC):
    """Class menu.
    """
    _title: str = ""
    _items: List[str] = []

    @abstractmethod
    def _draw_title(self) -> None:
        """Draws the menu title.
        """
        return

    @abstractmethod
    def _draw_items(self) -> None:
        """Draws the menu items.
        """
        return

    @abstractmethod
    def _draw_menu(self) -> int:
        """Draws the menu.
        """
        return

    @abstractmethod
    def _set_title(self) -> None:
        """Sets the menu title.
        """
        return

    @abstractmethod
    def _set_items(self) -> None:
        """Sets the menu items
        """
        return
