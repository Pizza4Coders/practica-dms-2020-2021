""" Rule class module.
"""

import json
from dms2021core.data.rest import RestResponse
from dms2021sensor.logic import RuleManager
from dms2021sensor.data.db.exc import RuleNotExistsError, RuleExistsError
from dms2021sensor.data.rest.exc import NotFoundError
from dms2021sensor.data.rest import AuthService
from dms2021core.data import UserRightName

class Rule():
    """ Class responsible of handling the log-related REST requests.
    """

    def __init__(self, rule_manager: RuleManager, auth_service: AuthService):
        """ Constructor method.

        Initializes the user REST interface.
        ---
        Parameters:
            - rule_manager: Instance responsible of the rule logic operations.
        """
        self.__set_rule_manager(rule_manager)
        self.__set_auth_service(auth_service)

    def get_rule_manager(self) -> RuleManager:
        """ Gets the rule manager object being used by this instance.
        ---
        Returns:
            The user manager instance in use.
        """
        return self.__rule_manager

    def __set_rule_manager(self, rule_manager: RuleManager):
        """ Sets the new user manager object to be used by this instance.
        ---
        Parameters:
            - rule_manager: The new rule manager instance.
        """
        self.__rule_manager = rule_manager

    def get_auth_service(self) -> AuthService:
        """ Gets the auth service object being used by this instance.
        ---
        Returns:
            The auth service instance in use.
        """
        return self.__auth_service

    def __set_auth_service(self, auth_service: AuthService):
        """ Sets the new user manager object to be used by this instance.
        ---
        Parameters:
            - rule_manager: The new rule manager instance.
        """
        self.__auth_service = auth_service

    def get_all_rules(self, user: str) -> RestResponse:
        """ Gets all rules.
        ---
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            if not self.get_auth_service().has_right(user, "AdminRules"):
                return RestResponse(code=401, mime_type="text/plain")
        except NotFoundError:
            return RestResponse(code=401, mime_type="text/plain")
        result = self.get_rule_manager().get_all_rules()
        json_content = [str(rule) for rule in result]
        json_response = json.dumps(json_content)
        return RestResponse(json_response, mime_type="application/json")

    def get_rule(self, rule_name: str, user: str) -> RestResponse:
        """ Gets a rule.
        ---
        Parameters:
            - rulename: The rule name string.
            - user: The username string.
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            if not self.get_auth_service().has_right(user, "AdminRules"):
                return RestResponse(code=401, mime_type="text/plain")
            result = self.get_rule_manager().get_rule(rule_name)
            json_response = json.dumps(str(result))
            return RestResponse(json_response, mime_type="application/json")
        except ValueError:
            return RestResponse(code=400, mime_type="text/plain")
        except RuleNotExistsError:
            return RestResponse(code=400, mime_type="text/plain")
        except NotFoundError:
            return RestResponse(code=401, mime_type="text/plain")

    def delete_rule(self, rule_name: str, user: str) -> RestResponse:
        """ Deletes a rule.
        ---
        Parameters:
            - rulename: The rule name string.
            - user: The username string.
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            if not self.get_auth_service().has_right(user, "AdminRules"):
                return RestResponse(code=401, mime_type="text/plain")
            self.get_rule_manager().delete_rule(rule_name)
        except ValueError:
            return RestResponse(code=400, mime_type="text/plain")
        except RuleNotExistsError:
            return RestResponse(code=404, mime_type="text/plain")
        except NotFoundError:
            return RestResponse(code=401, mime_type="text/plain")
        return RestResponse(mime_type="text/plain")

    def create_rule(self, rule_name:str, rule_type: str, data: str, frequency: int,
        user: str) -> RestResponse:
        """ Creates a rule.
        ---
        Parameters:
            - rulename: The rule name string.
            - ruletype: The type of the rule string. (text: command, file)
            - ruleargs: A command or a file path.
            - frequency (seconds): 0 if it does not execute automatically.
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            if not self.get_auth_service().has_right(user, "AdminRules"):
                return RestResponse(code=401, mime_type="text/plain")
            self.get_rule_manager().create_rule(rule_name, rule_type, data, frequency)
        except ValueError:
            return RestResponse(code=400, mime_type="text/plain")
        except RuleExistsError:
            return RestResponse(code=409, mime_type="text/plain")
        except NotFoundError:
            return RestResponse(code=401, mime_type="text/plain")
        return RestResponse(mime_type="text/plain")
