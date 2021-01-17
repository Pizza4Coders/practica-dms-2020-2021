""" Module containing the dms2021client.presentation.menus.ORderedMenu class
"""

from abc import ABC, abstractmethod
from typing import List, Callable, Union
from colorama import Fore, Style # type: ignore

class OrderedMenu(ABC):
    """Class Ordered Menu
    """

    _ordered_title: str = ""
    _ordered_items: List[str] = []
    _ordered_opt_functions: List[Callable] = []

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
        print(Style.BRIGHT + Fore.BLUE + "-"*20 + self._ordered_title + "-"*20
            + Style.RESET_ALL + "\n")

    def _draw_items(self) -> None:
        """ Display the menu items.
        """
        for i, item in enumerate(self._ordered_items, 1):
            print(Fore.CYAN + str(i) + ". " + item)
        print(Style.BRIGHT + Fore.BLUE + "\n" +"-"*(40+len(self._ordered_title)) + Style.RESET_ALL)

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
                if not self._ordered_items or not self._ordered_opt_functions:
                    return
                self._draw_title()
                self._draw_items()
                print(Fore.YELLOW + "Si desea volver atrás introduzca \"Salir\"")
                selected_opt = input(Fore.CYAN + "Selecciona una opción: " + Fore.RESET)
                if selected_opt.lower() in ("salir", "atrás", "exit", "back", "q"):
                    return
                selected_opt_num = int(selected_opt)
            except ValueError:
                continue
            if selected_opt_num <= 0 or selected_opt_num > len(self._ordered_items):
                self.print_error("Esa opción no es correcta.")
                continue
            self._ordered_opt_functions[int(selected_opt_num) - 1]()

    @classmethod
    def print_error(cls, error_text: str) -> None:
        """ Prints errors with style
        """
        print(Fore.RED + error_text + Fore.RESET)
