""" Mainmenu class module.
"""
from typing import List, Callable
from http.client import HTTPException
from getpass import getpass
from dms2021client.data.rest import AuthService, SensorsService
from dms2021client.data.rest.exc import BadRequestError, ConflictError, UnauthorizedError
from dms2021client.presentation.user_menus.modifyrightsmenu import ModifyRightsMenu
from dms2021client.presentation.sensor_menus import SensorsMenu
from dms2021client.presentation.orderedmenu import OrderedMenu

class MainMenu(OrderedMenu):
    """ Shows a menu with many options.
    """

    def __init__(self, session_token: str, username: str, auth_service: AuthService,
        sensors_services: List[SensorsService]):
        """ Constructor method.

        Initializes the MainMenu.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - username: The username of the user string.
            - auth_service: REST client to connect to the authentication service authservice.
            - sensors_services: REST client to connect the sensors services sensorservice.
        """
        self.__session_token = session_token
        self.__username = username
        self.__authservice = auth_service
        self.__sensorsservices = sensors_services

    def set_title(self) -> None:
        """ Sets the menu title.
        ---
        Parameters:
            - title: A string with the title that will be displayed in the menu.
        """
        self._ordered_title = "MENÚ PRINCIPAL"

    def set_items(self) -> None:
        """ Sets the menu items.
        ---
        Parameters:
            - items: A list with the strings that will display the menu options.
        """
        items: List[str] = []
        try:
            if self.__authservice.has_right(self.__username, "AdminUsers"):
                items.append("Crear usuarios")

            if self.__authservice.has_right(self.__username, "AdminRights"):
                items.append("Modificar permisos de usuarios")

            if self.__authservice.has_right(self.__username, "AdminSensors"):
                items.append("Gestionar sensores")
        except HTTPException:
            self.print_error("Ha ocurrido un error inesperado.")
            return
        self._ordered_items = items

    def set_opt_fuctions(self) -> None:
        """ Sets the function that will be executed when you select one option.
        Parameters:
            - functions: A list with the functions that will be called when
            a menu option is selected.
        """
        functions: List[Callable] = []
        try:
            if self.__authservice.has_right(self.__username, "AdminUsers"):
                functions.append(self.create_users)

            if self.__authservice.has_right(self.__username, "AdminRights"):
                functions.append(ModifyRightsMenu(self.__session_token,
                    self.__authservice).show_options)

            if self.__authservice.has_right(self.__username, "AdminSensors"):
                functions.append(SensorsMenu(self.__session_token, self.__username,
                    self.__authservice, self.__sensorsservices).show_options)
        except HTTPException:
            self.print_error("Ha ocurrido un error inesperado.")
            return
        self._ordered_opt_functions = functions

    def create_users(self):
        """ Allows to create a user.
        """
        username: str = input("Escriba el nombre del usuario a crear: ")
        password: str = getpass("Escriba la contraseña para el usuario: ")
        try:
            self.__authservice.create_user(username, password, self.__session_token)
            print("El usuario se ha creado correctamente.")
        except BadRequestError:
            self.print_error("Falta algún dato. Revíselo.")
        except UnauthorizedError:
            self.print_error("Usted no tiene permisos de usuarios.")
        except ConflictError:
            self.print_error("El usuario ya existe.")
        except HTTPException:
            self.print_error("Ha ocurrido un error inesperado.")
