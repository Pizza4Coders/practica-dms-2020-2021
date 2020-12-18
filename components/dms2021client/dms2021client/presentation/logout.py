""" Logout class module.
"""
from dms2021client.data.rest import AuthService
from dms2021client.data.rest.exc import UnauthorizedError
from dms2021client.presentation.menus import OrderedMenu

class Logout(OrderedMenu):
    """ Log out.
    """

    def __init__(self, session_token: str, authservice: AuthService):
        """ Constructor method.

        Initializes the variables.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - authservice: REST cliente to connect to the authentication service authservice.
        """
        self.__session_token: str = session_token
        self.__authservice: AuthService = authservice

    def show_options(self):
        """ Log out.
        """
        try:
            self.__authservice.logout(self.__session_token)
            print("La sesión se ha cerrado correctamente")
        except UnauthorizedError:
            print("Sesión incorrecta")
        except Exception:
            print("Ha ocurrido un error inesperado")

