""" GrantRevokeMenu class module.
"""
from functools import partial
from typing import List, Callable, Tuple
from http.client import HTTPException
from dms2021client.data.rest import AuthService
from dms2021client.presentation.orderedmenu import OrderedMenu
from dms2021client.data.rest.exc import NotFoundError, UnauthorizedError

class GrantRevokeMenu(OrderedMenu):
    """ Grant or revoke rights.
    """
    _username: str = ""

    def __init__(self, session_token: str, auth_service: AuthService, option: int):
        """ Constructor method.

        Initializes the variables.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - authservice: REST cliente to connect to the authentication service authservice.
            - option: 1, grant, 2, revoke.
        """
        self.__session_token: str = session_token
        self.__authservice: AuthService = auth_service
        self.__option: int = option
        self.__repeat = False

    def set_title(self) -> None:
        """ Sets the menu title.
        """
        if self.__option == 1:
            self._ordered_title = "AÑADIR PERMISOS"
        else:
            self._ordered_title = "ELIMINAR PERMISOS"

    def set_items(self) -> None:
        """ Sets the menu items.
        """
        if not self.__repeat:
            self._username: str = input("Introduzca el nombre del usuario: ")
        self._ordered_items = self.get_rights()[0]
        if not self._ordered_items:
            if self.__option == 1:
                print("El usuario ya tiene todos los permisos.")
                return
            print("El usuario no tiene ningún permiso.")
            return

    def set_opt_fuctions(self) -> None:
        """ Sets the function that will be executed when you select one option.
        """
        self._ordered_opt_functions = self.get_rights()[1]

    def get_rights(self) -> Tuple[List[str], List[Callable]]:
        """ Gets rights of a user (what he has or not depends on the option)
        ---
        Parameters:
            - param: 0, return the rights, 1, return the functions.
        Returns:
            - right_result: The rights a user has o not.
            - functions: The functions to execute.
        """
        rights: List[str] = ["AdminRights", "AdminUsers", "AdminRules", "AdminSensors",
        "ViewReports"]
        functions: List[Callable] = []
        right_result: List[str] = []

        for i in rights:
            if self.__authservice.has_right(self._username, i) and self.__option == 2:
                right_result.append(i)
                fun = partial(self.manage_rights, i, False)
                functions.append(fun)
            elif not self.__authservice.has_right(self._username, i) and self.__option == 1:
                right_result.append(i)
                fun = partial(self.manage_rights, i)
                functions.append(fun)
        return right_result, functions

    def manage_rights(self, right: str, grant: bool = True):
        """ Grants or revokes rights.
        ---
        Parameters:
            - right: Right to be revoked or granted.
            - grant: False, revoke, True, grant.
        """
        try:
            if not grant:
                self.__authservice.revoke(self._username, right, self.__session_token)
                print(f"El permiso {right} ha sido eliminado del usuario {self._username}.\n")
            else:
                self.__authservice.grant(self._username, right, self.__session_token)
                print(f"El permiso {right} ha sido añadido del usuario {self._username}.\n")
            self.__repeat = True
        except UnauthorizedError:
            print("Usted no tiene permiso para cambiar permisos.")
        except NotFoundError:
            print("No se pueden modificar permisos de un usuario inexistente.")
        except HTTPException:
            print("Ha ocurrido un error inesperado.")
