"""SensorsMenu class module.
"""

from typing import List, Callable
from dms2021client.data.rest import AuthService, SensorsService
from dms2021client.presentation.orderedmenu import OrderedMenu
from dms2021client.presentation.sensor_menus.rulesmenu import RulesMenu

class SensorsMenu(OrderedMenu):
    """ Grants or revokes rights.
    """

    def __init__(self, session_token: str, username: str,
        authservice: AuthService, sensorsservices: List[SensorsService]):
        """ Constructor method.

        Initializes the variables.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - username: The username string.
            - authservice: REST cliente to connect to the authentication service authservice.
            - sensorservices: REST cliente to connect to the sensorentication service sensorservice.
        """
        self.__session_token: str = session_token
        self.__username: str = username
        self.__authservice: AuthService = authservice
        self.__sensorservices: List[SensorsService] = sensorsservices

    def set_title(self) -> None:
        """ Sets the menu title.
        ---
        Parameters:
            - title: A string with the title that will be displayed in the menu.
        """
        self._ordered_title = "MENÚ SENSORES"

    def set_items(self) -> None:
        """ Sets the menu items.
        ---
        Parameters:
            - items: A list with the strings that will display the menu options.
        """
        items: List[str] = []
        for i in range(1, len(self.__sensorservices) + 1):
            items.append("Sensor " + str(i))
        self._ordered_items = items

    def set_opt_fuctions(self) -> None:
        """ Sets the function that will be executed when you select one option.
        Parameters:
            - functions: A list with the functions that will be called when
            a menu option is selected.
        """
        functions: List[Callable] = []
        for sensorservice in self.__sensorservices:
            functions.append(RulesMenu(self.__session_token, self.__username,
                self.__authservice, sensorservice).show_options)
        self._ordered_opt_functions = functions
