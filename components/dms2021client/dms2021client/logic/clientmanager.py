""" Clientmanager class module.
"""
import time
from typing import Tuple
from getpass import getpass
from http.client import HTTPException
from dms2021client.data.config import ClientConfiguration
from dms2021client.data.rest import AuthService, SensorsService
from dms2021client.data.rest.exc import InvalidCredentialsError, UnauthorizedError
from dms2021client.presentation import OrderedMenu, MainMenu

class ClientManager():
    """ Manager class for the client logic.
    """

    def __init__(self):
        """ Constructor method.

        Initializes the ClientManager.
        """
        self.__cfg: ClientConfiguration = ClientConfiguration()
        self.__cfg.load_from_file(self.__cfg.default_config_file())
        self.__authservice: AuthService = AuthService(self.__cfg.get_auth_service_host(),
            self.__cfg.get_auth_service_port())
        self.__sensor1_svc: SensorsService = SensorsService(
            self.__cfg.get_sensor1_service_host(),
            self.__cfg.get_sensor1_service_port()
        )
        self.__sensor2_svc: SensorsService = SensorsService(
            self.__cfg.get_sensor2_service_host(),
            self.__cfg.get_sensor2_service_port()
        )

        while True:
            self.__username, self.__session_id = self.login()

            self.__page: OrderedMenu = MainMenu(self.__session_id,
                self.__username, self.__authservice, [self.__sensor1_svc, self.__sensor2_svc])

            self.__page.show_options()

            self.logout()


    def login(self) -> Tuple[str, str]:
        """ Allows to enter the application.
        ---
        Returns:
            - username: The username string.
            - session_id: The session_id string.
        """
        while not self.__authservice.is_running():
            time.sleep(1)
        print("\nEl servicio de autenticación está activo.")

        print("Si desea salir pulse Ctrl+P, Ctrl+Q")
        while True:
            print("\nINICIO DE SESIÓN")
            username: str = input("Usuario: ")
            password: str = getpass("Contraseña: ")
            try:
                session_id: str = self.__authservice.login(username, password)
                print("Ha iniciado sesión correctamente " + username
                + " . Session id: " + session_id)
                break
            except InvalidCredentialsError:
                print("Usuario y/o contraseña. Vuelva a intentarlo.")
            except HTTPException as ex:
                print(ex)
        return username, session_id

    def logout(self):
        """ Allows to log out the application.
        """
        try:
            self.__authservice.logout(self.__session_id)
            print("La sesión se ha cerrado correctamente")
        except UnauthorizedError:
            print("Sesión incorrecta")
        except HTTPException:
            print("Ha ocurrido un error inesperado")
