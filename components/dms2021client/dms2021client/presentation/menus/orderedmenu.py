"""Ordered Menu Class
"""

from dms2021client.presentation.menus import Menu

class OrderedMenu(Menu):
    """Class Ordered Menu
    """
    _ordered_title = ""
    _ordered_items = []

    def _draw_title(self) -> None:
        """Draws the menu title.
        """
        print("-"*20 + self._ordered_title + "-"*20 + "\n")

    def _draw_items(self) -> None:
        """Draws the menu items.
        """
        for i, item in enumerate(self._ordered_items, 1):
            print(i + ". " + item)

    def _draw_menu(self) -> int:
        """Draws the menu.
        """
        self._draw_title()
        self._draw_items()
        print("-"*(40+len(self._ordered_title)))
        selected_opt = input("Select an option from above: ")
        return selected_opt

    def _set_title(self) -> None:
        """Sets the menu title.
        """
        self._ordered_title = ""

    def _set_items(self) -> None:
        """Sets the menu items.
        """
        self._ordered_items = []
