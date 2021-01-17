""" Module containing the dms2021client.presentation.menus.ORderedMenu class
"""

from abc import ABC, abstractmethod
from typing import List, Callable, Union

class OrderedMenu(ABC):
    """Class Ordered Menu
    """

    _ordered_title: str = ""
    _ordered_items: List[str] = []
    _ordered_opt_functions: List[Callable] = []
    _returning: bool = False

    @abstractmethod
    def set_title(self) -> None:
        """ Sets the menu title.
        ---
        Parameters:
            - title: A string with the title that will be displayed in the menu.
        """
        return

    @abstractmethod
    def set_items(self) -> None:
        """ Sets the menu items.
        ---
        Parameters:
            - items: A list with the strings that will display the menu options.
        """
        return

    @abstractmethod
    def set_opt_fuctions(self) -> None:
        """ Sets the function that will be executed when you select one option.
        Parameters:
            - functions: A list with the functions that will be called when
            a menu option is selected.
        """
        return

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

    def _load_menu(self) -> None:
        """ Loads menu data.
        """
        self.set_title()
        self.set_items()
        self.set_opt_fuctions()

    def show_options(self) -> None:
        """ Display the menu and controls the actions to be executed when one option
        have been selected.
        """
        selected_opt: Union[str, int] = 0
        while True:
            try:
                self._load_menu()
                self._draw_title()
                self._draw_items()
                print("Si desea volver atrás introduzca \"Salir\"")
                selected_opt = input("Selecciona una opción: ")
                if selected_opt.lower() in ("salir", "atrás", "exit", "back", "q"):
                    self._returning = True
                    return
                selected_opt_num = int(selected_opt)
            except ValueError:
                continue
            if selected_opt_num <= 0 or selected_opt_num > len(self._ordered_items):
                print("Esa opción no es correcta.")
                continue
            self._ordered_opt_functions[int(selected_opt_num) - 1]()
            return
