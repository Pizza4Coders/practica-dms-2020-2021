""" Mainmenu class module.
"""
from typing import List, Callable
from http.client import HTTPException
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

    def show_options(self) -> None:
        """ Shows the options of the menu depends on the rights the user has.
        """
        options: List[str] = []
        functions: List[Callable] = []

        super().set_title("MENÚ PRINCIPAL")
        if self.__authservice.has_right(self.__username, "AdminUsers"):
            options.append("Crear usuarios")
            functions.append(self.create_users())

        if self.__authservice.has_right(self.__username, "AdminRights"):
            options.append("Modificar permisos de usuarios")
            functions.append(ModifyRightsMenu(self.__session_token,
                self.__authservice).show_options())

        if (self.__authservice.has_right(self.__username, "AdminSensors") or
        self.__authservice.has_right(self.__username, "AdminRules") or
        self.__authservice.has_right(self.__username, "ViewReports")):
            options.append("Gestionar sensores")
            functions.append(SensorsMenu(self.__session_token, self.__username,
                self.__authservice, self.__sensorsservices).show_options())

        super().set_items(options)
        super().set_opt_fuctions(functions)
        super().show_options()

    def create_users(self):
        """ Allows to create a user.
        """
        username: str = input("Escriba el nombre del usuario a crear: ")
        password: str = input("Escriba la contraseña para el usuario: ")
        try:
            self.__authservice.create_user(username, password, self.__session_token)
            print("El usuario se ha creado correctamente.")
        except BadRequestError:
            print("Falta algún dato. Revíselo.")
        except UnauthorizedError:
            print("Usted no tiene permisos de usuarios.")
        except ConflictError:
            print("El usuario ya existe.")
        except HTTPException:
            print("Ha ocurrido un error inesperado.")
