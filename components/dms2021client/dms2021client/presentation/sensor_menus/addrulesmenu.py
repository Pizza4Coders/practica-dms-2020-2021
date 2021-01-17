""" AddRulesMenu class module.
"""

from typing import List, Callable
from http.client import HTTPException
from dms2021client.data.rest.exc import BadRequestError, ConflictError, UnauthorizedError
from dms2021client.data.rest import AuthService, SensorsService
from dms2021client.presentation.orderedmenu import OrderedMenu

class AddRulesMenu(OrderedMenu):
    """ Add Rules.
    """

    def __init__(self, session_token: str, username: str,
        authservice: AuthService, sensorservice: SensorsService):
        """ Constructor method.

        Initializes the variables.
        ---
        Parameters:
            - session_token: The session_token of the user string.
            - username: The username string.
            - authservice: REST cliente to connect to the authentication service authservice.
            - sensorservice: REST cliente to connect to the sensorentication service sensorservice.
        """
        self.__session_token: str = session_token
        self.__username: str = username
        self.__authservice: AuthService = authservice
        self.__sensorservice: SensorsService = sensorservice

    def show_options(self):
        """ Shows options to modify rules or view reports, depends on the rights
        the user has.
        """
        while not self._returning:
            options: List[str] = []
            functions: List[Callable] = []

            self.set_title("SELECCIONE EL TIPO DE REGLA A AÑADIR")
            if self.__authservice.has_right(self.__username, "AdminRules"):
                options += ["Fichero. Comprueba la existencia de un fichero",
                "Comando. Ejecuta un comando Linux", "CPU. Comprueba el uso de la cpu"]
                functions += [self.add_file_rule, self.add_command_rule, self.add_cpu_rule]
            super().set_items(options)
            super().set_opt_fuctions(functions)
            try:
                super().show_options()
            except BadRequestError:
                print("Se han introducido parámetros incorrectos.")
            except UnauthorizedError:
                print("Usted no tiene permisos para realizar esta acción.")
            except ConflictError:
                print("Ya existe una regla con ese nombre.")
            except HTTPException:
                print("Ha ocurrido un error inesperado.")

    def add_rules(self, rulename: str, ruletype: str, ruleargs: str) -> None:
        """ Creates a new rule.
        """
        frequency: int
        while True:
            try:
                frequency = int(input("Introduzca la frecuencia de ejecución en segundos: "))
                break
            except ValueError:
                print("Valor incorrecto.")
        self.__sensorservice.create_rule(rulename, ruletype, ruleargs, frequency, self.__username)
        print("\n La regla " + rulename + " ha sido creada correctamente.")

    def add_file_rule(self) -> None:
        """ Creates a new file checking rule.
        """
        rulename: str = input("Introduzca el nombre de la regla: ")
        ruleargs: str = input("Introduzca la ruta al fichero que desee comprobar: ")
        self.add_rules(rulename, "file", ruleargs)

    def add_command_rule(self) -> None:
        """ Creates a new command rule.
        """
        rulename: str = input("Introduzca el nombre de la regla: ")
        ruleargs: str = input("Introduzca el comando Linux que desee ejecutar: ")
        self.add_rules(rulename, "command", ruleargs)

    def add_cpu_rule(self) -> None:
        """ Creates a new cpu rule.
        """
        rulename: str = input("Introduzca el nombre de la regla: ")
        ruleargs: str = input("Introduzca el número de core que desee comprobar \
        o 'all' si desea comprobar todos a la vez: ")
        self.add_rules(rulename, "cpu", ruleargs)
