""" Createuser class module.
"""
from dms2021client.data.rest import AuthService
from dms2021client.data.rest.exc import BadRequestError, ConflictError, UnauthorizedError
from dms2021client.presentation.orderedmenu import OrderedMenu

class CreateUserMenu(OrderedMenu):
    """ Allows the creation of a user.
    """

    def __init__(self, session_token: str, username: str, authservice: AuthService):
        """ Constructor method.

        Initializes the variables.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - username: The username string.
            - authservice: REST cliente to connect to the authentication service authservice.
        """
        self.__session_token: str = session_token
        self.__username: str = username
        self.__authservice: AuthService = authservice

    def shows_options(self):
        """ Creates a user.
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
        except Exception:
            print("Ha ocurrido un error inesperado.")
