""" RulesMenu class module.
"""

from typing import List, Callable
from http.client import HTTPException
from dms2021client.data.rest.exc import BadRequestError, NotFoundError
from dms2021client.data.rest.exc import UnauthorizedError
from dms2021client.data.rest import AuthService, SensorsService
from dms2021client.presentation.sensor_menus.addrulesmenu import AddRulesMenu
from dms2021client.presentation.orderedmenu import OrderedMenu

class RulesMenu(OrderedMenu):
    """ Add, Remove, Show or Execute Rules.
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

    def set_title(self) -> None:
        """ Sets the menu title.
        ---
        Parameters:
            - title: A string with the title that will be displayed in the menu.
        """
        self._ordered_title = "MENÚ REGLAS"

    def set_items(self) -> None:
        """ Sets the menu items.
        ---
        Parameters:
            - items: A list with the strings that will display the menu options.
        """
        items: List[str] = []
        if self.__authservice.has_right(self.__username, "AdminRules"):
            items += ["Ver reglas", "Añadir regla", "Eliminar regla"]
            if self.__authservice.has_right(self.__username, "ViewReports"):
                items.append("Ejecutar regla")
        if self.__authservice.has_right(self.__username, "ViewReports"):
            items.append("Ver historial de ejecución")
        self._ordered_items = items

    def set_opt_fuctions(self) -> None:
        """ Sets the function that will be executed when you select one option.
        Parameters:
            - functions: A list with the functions that will be called when
            a menu option is selected.
        """
        functions: List[Callable] = []
        if self.__authservice.has_right(self.__username, "AdminRules"):
            functions += [self.get_rules,
                AddRulesMenu(self.__session_token, self.__username,
                self.__authservice, self.__sensorservice).show_options,
                self.remove_rules]
            if self.__authservice.has_right(self.__username, "ViewReports"):
                functions.append(self.run_rule)
        if self.__authservice.has_right(self.__username, "ViewReports"):
            functions.append(self.get_log)
        self._ordered_opt_functions = functions

    def get_rules(self) -> None:
        """ Gets the list of rules.
        """
        print("-"*20 + "VER REGLAS" + "-"*20 + "\n")
        try:
            result: List[dict] = self.__sensorservice.get_all_rules(self.__username)
            for rule in result:
                for k in rule:
                    print("[" + k.upper() + "] -> " + str(rule[k]))
                print("-"*50)
        except UnauthorizedError:
            print("Usted no tiene permisos para realizar esta acción.")
        except HTTPException:
            print("Ha ocurrido un error inesperado.")

    def remove_rules(self) -> None:
        """ Removes a specified rule.
        """
        try:
            print("-"*20 + "ELIMINAR REGLA" + "-"*20 + "\n")
            rulename: str = input("Introduzca el nombre de la regla: ")
            self.__sensorservice.delete_rule(rulename, self.__username)
            print("\n La regla " + rulename + " ha sido eliminada correctamente.")
        except BadRequestError:
            print("Se han introducido parámetros incorrectos.")
        except UnauthorizedError:
            print("Usted no tiene permisos para realizar esta acción.")
        except NotFoundError:
            print("No existe una regla con ese nombre.")
        except HTTPException:
            print("Ha ocurrido un error inesperado.")

    def run_rule(self) -> None:
        """ Runs a specified rule.
        """
        try:
            print("-"*20 + "EJECUTAR REGLA" + "-"*20 + "\n")
            rulename: str = input("Introduzca el nombre de la regla: ")
            result: dict = self.__sensorservice.run_rule(rulename, self.__username)
            print("Resultado de la ejecución: ")
            print(result["result"])
        except BadRequestError:
            print("Se han introducido parámetros incorrectos.")
        except UnauthorizedError:
            print("Usted no tiene permisos para realizar esta acción.")
        except NotFoundError:
            print("No existe una regla con ese nombre.")
        except HTTPException:
            print("Ha ocurrido un error inesperado.")

    def get_log(self) -> None:
        """ Gets the log.
        """
        try:
            print("-"*20 + "VER HISTORIAL DE EJECUCIÓN" + "-"*20 + "\n")
            result: List[dict] = self.__sensorservice.get_log(self.__username)
            for rule in result:
                for k in rule:
                    print("[" + k.upper() + "] -> " + str(rule[k]))
                print("-"*66)
        except UnauthorizedError:
            print("Usted no tiene permisos para realizar esta acción.")
        except HTTPException:
            print("Ha ocurrido un error inesperado.")
