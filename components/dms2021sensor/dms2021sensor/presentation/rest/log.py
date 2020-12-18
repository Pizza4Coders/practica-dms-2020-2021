""" Log class module.
"""

import json
from dms2021core.data.rest import RestResponse
from dms2021sensor.logic import RuleManager, LogManager
from dms2021sensor.data.db.exc import RuleNotExistsError
from dms2021sensor.logic.rulerunners.exc import RuleRunError
from dms2021sensor.data.rest.exc import NotFoundError
from dms2021sensor.data.rest import AuthService
from dms2021core.data import UserRightName

class Log():
    """ Class responsible of handling the log-related REST requests.
    """

    def __init__(self, rule_manager: RuleManager, log_manager: LogManager, auth_service: AuthService):
        """ Constructor method.

        Initializes the user REST interface.
        ---
        Parameters:
            - rule_manager: Instance responsible of the rule logic operations.
            - log_manager: Instance responsible of the log logic operations.
        """
        self.__set_rule_manager(rule_manager)
        self.__set_log_manager(log_manager)
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

    def get_log_manager(self) -> LogManager:
        """ Gets the log manager object being used by this instance.
        ---
        Returns:
            The log manager instance in use.
        """
        return self.__log_manager

    def __set_log_manager(self, log_manager: LogManager):
        """ Sets the new user manager object to be used by this instance.
        ---
        Parameters:
            - log_manager: The new log manager instance.
        """
        self.__log_manager = log_manager

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

    def run_rule(self, rule_name: str, user: str) -> RestResponse:
        """ Creates a new user.
        ---
        Parameters:
            - username: The rule name string.
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            if not self.get_auth_service().has_right(user, "AdminRules"):
                return RestResponse(code=401, mime_type="text/plain")
            if not self.get_auth_service().has_right(user, "ViewReports"):
                return RestResponse(code=401, mime_type="text/plain")
            result = self.get_rule_manager().run_rule(rule_name, self.get_log_manager())
            json_content = {"result": result}
            json_response = json.dumps(json_content)
            return RestResponse(json_response, mime_type="application/json")
        except ValueError:
            return RestResponse(code=400, mime_type='text/plain')
        except RuleNotExistsError:
            return RestResponse(code=404, mime_type='text/plain')
        except RuleRunError:
            return RestResponse(code=500, mime_type="text/plain")
        except NotFoundError:
            return RestResponse(code=401, mime_type="text/plain")

    def get_log(self, user: str) -> RestResponse:
        """ Gets the log.
        ---
        Returns:
            A RestResponse object holding the result of the operation.
        """
        try:
            if not self.get_auth_service().has_right(user, "ViewReports"):
                return RestResponse(code=401, mime_type="text/plain")
        except NotFoundError:
            return RestResponse(code=401, mime_type="text/plain")
        result = self.get_log_manager().get_all_runs()
        json_content = [str(log) for log in result]
        json_response = json.dumps(json_content)
        return RestResponse(json_response, mime_type="application/json")
