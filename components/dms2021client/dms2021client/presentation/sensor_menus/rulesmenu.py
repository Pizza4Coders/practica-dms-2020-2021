"""RulesMenu class module.
"""

from typing import List, Callable
from http.client import HTTPException
from dms2021client.data.rest.exc import BadRequestError, ConflictError, NotFoundError
from dms2021client.data.rest.exc import UnauthorizedError
from dms2021client.data.rest import AuthService, SensorsService
from dms2021client.presentation.orderedmenu import OrderedMenu

class RulesMenu(OrderedMenu):
    """ Add, Remove, Show or Execute Rules
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

    def show_options(self) -> None:
        options: List[str] = []
        functions: List[Callable]

        self.set_title("MENÚ REGLAS")
        if self.__authservice.has_right(self.__username, "AdminRules"):
            options += ["Ver reglas", "Añadir regla", "Eliminar regla"]
            functions += [self.get_rules, self.add_rules, self.remove_rules]
            if self.__authservice.has_right(self.__username, "ViewReports"):
                options.append("Ejecutar regla")
                functions.append(self.run_rule)
        if self.__authservice.has_right(self.__username, "ViewReports"):
            options.append("Ver historial de ejecución")
            functions.append(self.get_log)
        super().set_items(options)
        super().set_opt_fuctions(functions)
        try:
            super().show_options()
        except BadRequestError:
            print("Se han introducido parámetros incorrectos.")
        except UnauthorizedError:
            print("Usted no tiene permisos para realizar esta acción.")
        except NotFoundError:
            print("No existe una regla con ese nombre.")
        except ConflictError:
            print("Ya existe una regla con ese nombre.")
        except HTTPException:
            print("Ha ocurrido un error inesperado.")

    def get_rules(self) -> None:
        """ Gets the list of rules.
        """
        print("-"*20 + "VER REGLAS" + "-"*20 + "\n")
        result: List[dict] = self.__sensorservice.get_all_rules(self.__username)
        for rule in result:
            for k, val in rule:
                print("[" + k.upper() + "] -> " + str(val))
            print("-"*50)

    def add_rules(self) -> None:
        """ Creates a new rule.
        """
        print("-"*20 + "AÑADIR REGLA" + "-"*20 + "\n")
        rulename: str = input("Introduzca el nombre de la regla: ")
        ruletype: str = input("Introduzca el tipo de la regla (tipos de regla): ")
        ruleargs: str = input("Introduzca los argumentos de la regla (ejemplo): ")
        frequency: int
        while True:
            try:
                frequency = int(input("Introduzca la frecuencia de ejecución en segundos: "))
                break
            except ValueError:
                print("Valor incorrecto.")
        self.__sensorservice.create_rule(rulename, ruletype, ruleargs,
            frequency, self.__username)
        print("\n La regla " + rulename + " ha sido creada correctamente.")

    def remove_rules(self) -> None:
        """ Removes a specified rule.
        """
        print("-"*20 + "ELIMINAR REGLA" + "-"*20 + "\n")
        rulename: str = input("Introduzca el nombre de la regla: ")
        self.__sensorservice.delete_rule(rulename, self.__username)
        print("\n La regla " + rulename + " ha sido eliminada correctamente.")

    def run_rule(self) -> None:
        """ Runs a specified rule.
        """
        print("-"*20 + "EJECUTAR REGLA" + "-"*20 + "\n")
        rulename: str = input("Introduzca el nombre de la regla: ")
        result: dict = self.__sensorservice.run_rule(rulename, self.__username)
        print("Resultado de la ejecución: ")
        for k, val in result:
            print("[" + k.upper() + "] -> " + str(val))

    def get_log(self) -> None:
        """ Gets the log.
        """
        print("-"*20 + "VER HISTORIAL DE EJECUCIÓN" + "-"*20 + "\n")
        result: List[dict] = self.__sensorservice.get_log(self.__username)
        for rule in result:
            for k, val in rule:
                print("[" + k.upper() + "] -> " + str(val))
            print("-"*66)
