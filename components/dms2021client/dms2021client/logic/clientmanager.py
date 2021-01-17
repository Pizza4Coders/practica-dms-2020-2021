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
from colorama import Fore, Style # type: ignore

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
        print(Style.BRIGHT + Fore.GREEN + "\nEl servicio de autenticación está activo.")

        print(Fore.YELLOW + "Si desea salir pulse Ctrl+P, Ctrl+Q" + Fore.RESET)
        while True:
            print(Fore.BLUE + "\nINICIO DE SESIÓN" + Style.RESET_ALL)
            username: str = input("Usuario: ")
            password: str = getpass("Contraseña: ")
            try:
                session_id: str = self.__authservice.login(username, password)
                print(Fore.GREEN + "Ha iniciado sesión correctamente " +
                    Fore.RESET + username + " . Session id: " + session_id)
                break
            except InvalidCredentialsError:
                print(Fore.RED + "Usuario y/o contraseña. Vuelva a intentarlo." + Style.RESET_ALL)
            except HTTPException as ex:
                print(ex)
        return username, session_id

    def logout(self):
        """ Allows to log out the application.
        """
        try:
            self.__authservice.logout(self.__session_id)
            print(Style.BRIGHT + Fore.GREEN + "La sesión se ha cerrado correctamente"
                + Style.RESET_ALL)
        except UnauthorizedError:
            print(Fore.RED + "Sesión incorrecta" + Fore.RESET)
        except HTTPException:
            print(Fore.RED + "Ha ocurrido un error inesperado" + Fore.RESET)
