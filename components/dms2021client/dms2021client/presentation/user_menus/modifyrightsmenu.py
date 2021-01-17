""" Modifyrights class module.
"""
from dms2021client.data.rest import AuthService
from dms2021client.presentation.orderedmenu import OrderedMenu
from dms2021client.presentation.user_menus import GrantRevokeMenu

class ModifyRightsMenu(OrderedMenu):
    """ Modify rights.
    """

    def __init__(self, session_token: str, auth_service: AuthService):
        """ Constructor method.

        Initializes the variables.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - authservice: REST cliente to connect to the authentication service authservice.
        """
        self.__session_token: str = session_token
        self.__authservice: AuthService = auth_service

    def set_title(self) -> None:
        """ Sets the menu title.
        """
        self._ordered_title = "MODIFICAR PERMISOS"

    def set_items(self) -> None:
        """ Sets the menu items.
        """
        self._ordered_items = ["Añadir permisos", "Eliminar permisos"]

    def set_opt_fuctions(self) -> None:
        """ Sets the function that will be executed when you select one option.
        """
        self._ordered_opt_functions = [
            GrantRevokeMenu(self.__session_token, self.__authservice, 1).show_options,
            GrantRevokeMenu(self.__session_token, self.__authservice, 2).show_options]
