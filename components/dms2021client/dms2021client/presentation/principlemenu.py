""" Principlemenu class module.
"""
from typing import List, Callable
from dms2021core.data import UserRightName
from dms2021client.data.rest import AuthService
from dms2021client.presentation import CreateUser, ModifyRights, Logout
from .menus import OrderedMenu

class PrincipleMenu(OrderedMenu):
    """ Shows a menu with many options.
    """

    def __init__(self, session_token: str, username: str, auth_service: AuthService):
        """ Constructor method.

        Initializes the PrincipleMenu.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - username: The username of the user string.
            - authservice: REST cliente to connect to the authentication service authservice.
        """
        self.__session_token = session_token
        self.__username = username
        self.__authservice = auth_service

    def show_options(self):
        """ Shows the options of the menu depends on the rights the user has.
        """
        options: List[str] = []
        functions: List[Callable]
        if self.__authservice.has_right(self.__username, "AdminUsers"):
            options.append("Crear usuarios")
            functions.append(CreateUser(self.__session_token, self.__username,
            self.__authservice).show_options())

        if self.__authservice.has_right(self.__username, "AdminRights"):
            options.append("Modificar permisos de usuarios")
            functions.append(ModifyRights(self.__session_token,
            self.__username, self.__authservice).show_options())

        if (self.__authservice.has_right(self.__username, "AdminSensors") or
        self.__authservice.has_right(self.__username, "AdminRules") or
        self.__authservice.has_right(self.__username, "ViewReports")):
            options.append("Gestionar sensores")
            #print("FALTA AÑADIR LLAMADA A CLASE")

        options.append("Cerrar sesión")
        functions.append(Logout(self.__session_token, self.__authservice).show_options())
        super().set_items(options)
        super().set_opt_fuctions(functions)
        super().show_options()
