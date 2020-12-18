""" Module containing the dms2021client.presentation.menus.Menu class
"""

from abc import ABC, abstractmethod
from typing import List, Callable

class Menu(ABC):
    """ Class responsible of creating menus.
    """

    _title: str = ""
    _items: List[str] = []
    _opt_functions: List[Callable] = []

    @abstractmethod
    def set_title(self, title: str) -> None:
        """ Sets the menu title.

        Subclasses are expected to override this method and provide their own
        implementation.
        ---
        Parameters:
            - title: A string with the title that will be displayed in the menu.
        """
        return

    @abstractmethod
    def set_items(self, items: List[str]) -> None:
        """ Sets the menu items.

        Subclasses are expected to override this method and provide their own
        implementation.
        ---
        Parameters:
            - items: A list with the strings that will display the menu options.
        """
        return

    @abstractmethod
    def set_opt_fuctions(self, functions: List[Callable]) -> None:
        """ Sets the functions that will be executed when you select one option.

        Subclasses are expected to override this method and provide their own
        implementation.
        ---
        Parameters:
            - functions: A list with the functions that will be called when
            a menu option is selected.
        """
        return

    @abstractmethod
    def _draw_title(self) -> None:
        """ Display the menu title.

        Subclasses are expected to override this method and provide their own
        implementation.
        """
        return

    @abstractmethod
    def _draw_items(self) -> None:
        """ Display the menu items.

        Subclasses are expected to override this method and provide their own
        implementation.
        """
        return

    @abstractmethod
    def show_options(self) -> None:
        """ Display the menu and controls the actions to be executed when one option
        have been selected.

        Subclasses are expected to override this method and provide their own
        implementation.
        """
        return
