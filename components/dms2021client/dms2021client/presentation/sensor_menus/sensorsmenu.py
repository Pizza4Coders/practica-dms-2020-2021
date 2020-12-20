"""SensorsMenu class module.
"""

from typing import List, Callable
from dms2021client.data.rest.exc import UnauthorizedError
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

    def show_options(self):
        """ Shows options to choose a sensor.
        """
        while not self._returning:
            options: List[str] = []
            functions: List[Callable] = []

            self.set_title("MENÚ SENSORES")
            for i, sensorservice in enumerate(self.__sensorservices, 1):
                options.append("Sensor " + str(i))
                functions.append(RulesMenu(self.__session_token, self.__username,
                    self.__authservice, sensorservice).show_options)
            self.set_items(options)
            self.set_opt_fuctions(functions)
            try:
                super().show_options()
            except UnauthorizedError:
                print("Usted no tiene permisos sobre este sensor.")
                self._returning = True
