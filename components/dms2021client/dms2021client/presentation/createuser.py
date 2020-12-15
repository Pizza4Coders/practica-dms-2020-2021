""" Createuser class module.
"""
from dms2021client.data.rest import AuthService

class CreateUser():
    """ Allows the creation of a user.
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

    def create_user(self):
        """ Creates a user.
        """
        print("*********CREACIÓN DE USUARIOS*********")
        username: str = input("Escriba el nombre del usuario a crear: ")
        password: str = input("Escriba la contraseña para el usuario: ")
        self.__authservice.create_user(username, password, self.__session_token)
        print("El usuario se ha creado correctamente")
