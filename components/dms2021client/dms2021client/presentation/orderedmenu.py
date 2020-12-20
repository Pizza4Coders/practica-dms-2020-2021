"""OrderedMenu class module.
"""

from typing import List, Callable, Union
from dms2021client.presentation.menu import Menu

class OrderedMenu(Menu):
    """Class Ordered Menu
    """

    _ordered_title: str = ""
    _ordered_items: List[str] = []
    _ordered_opt_functions: List[Callable] = []

    def set_title(self, title: str) -> None:
        """ Sets the menu title.
        ---
        Parameters:
            - title: A string with the title that will be displayed in the menu.
        """
        self._ordered_title = title

    def set_items(self, items: List[str]) -> None:
        """ Sets the menu items.
        ---
        Parameters:
            - items: A list with the strings that will display the menu options.
        """
        self._ordered_items = items

    def set_opt_fuctions(self, functions: List[Callable]) -> None:
        """ Sets the function that will be executed when you select one option.
        Parameters:
            - functions: A list with the functions that will be called when
            a menu option is selected.
        """
        self._ordered_opt_functions = functions

    def _draw_title(self) -> None:
        """ Display the menu title.
        """
        print("-"*20 + self._ordered_title + "-"*20 + "\n")

    def _draw_items(self) -> None:
        """ Display the menu items.
        """
        for i, item in enumerate(self._ordered_items, 1):
            print(str(i) + ". " + item)
        print("-"*(40+len(self._ordered_title)))

    def show_options(self) -> None:
        """ Display the menu and controls the actions to be executed when one option
        have been selected.
        """
        selected_opt: Union[str, int] = 0
        while True:
            try:
                self._draw_title()
                self._draw_items()
                print("Si desea volver atrás introduzca \"Salir\"")
                selected_opt = input("Selecciona una opción: ")
                if selected_opt.lower() in ("salir", "atrás", "exit", "back", "q"):
                    return
                selected_opt = int(selected_opt)
            except ValueError:
                pass
            self._ordered_opt_functions[int(selected_opt) - 1]()
