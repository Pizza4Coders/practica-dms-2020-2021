""" AuthService class module.
"""

import json
from urllib.parse import urlencode
from http.client import HTTPConnection, HTTPResponse, HTTPException
from dms2021client.data.rest.exc import InvalidCredentialsError, UnauthorizedError


class SensorsService():
    """ REST client to connect to the authentication service.
    """

    def __init__(self, host: str, port: int):
        """ Constructor method.

        Initializes the client.
        ---
        Parameters:
            - host: The authentication service host string.
            - port: The authentication service port number.
        """
        self.__host: str = host
        self.__port: int = port

    def __get_connection(self) -> HTTPConnection:
        """ Creates a new connection to the authentication server.
        ---
        Returns:
            The connection object.
        """
        return HTTPConnection(self.__host, self.__port)

    def is_running(self) -> bool:
        """ Tests whether the authentication service is running or not.
        ---
        Returns:
            True if the authentication service could be contacted successfully; false otherwise.
        """
        try:
            connection: HTTPConnection = self.__get_connection()
            connection.request('GET', '/')
            response: HTTPResponse = connection.getresponse()
            if response.status == 200:
                return True
            return False
        except HTTPException:
            return False
        except ConnectionRefusedError:
            return False
    
    def get_all_rules(self):
        """ Get the list of rules.
        ---
        Returns:
            A dictionary with the list of rules, where each has rule_name, type,
            data and frequency
        Throws:
            - HTTPException: On an unhandled 500 error.
        """


    def get_rule(self, rulename: str):
        """ Get the specified rule.
        ---
        Parameters:
            - rulename: The rule name string.
        Returns:
            A dictionary with a rule, where it has rule_name, type,
            data and frequency
        Throws:
            - BadRequestError: If the request is malformed.
            - NotFoundError: If the rule does not exist.
            - HTTPException: On an unhandled 500 error.
        """

    def create_rule(self, rulename: str, ruletype: str, ruleargs: str, frequency: int):
        """ Create a new rule.
        ---
        Parameters:
            - rulename: The rule name string.
            - ruletype: The type of the rule string. (text: command, file)
            - ruleargs: A command or a file path.
            - frequency (seconds): 0 if it does not execute automatically.
        Throws:
            - BadRequestError: If the request is malformed.
            - ConflictError: If the rule already exists.
            - HTTPException: On an unhandled 500 error.
        """

    def delete_rule(self, rulename: str):
        """ Removes a specified rule.
        ---
        Parameters:
            - rulename: The rule name string.
        Throws:
            - BadRequestError: If the request is malformed.
            - NotFoundError: If the rule does not exist.
            - HTTPException: On an unhandled 500 error.
        """

    def run_rule(self, rulename: str):
        """ Runs a specified rule.
        ---
        Parameters:
            - rulename: The rule name string.
        Returns:
            A dictionary with the output (str).
        Throws:
            - BadRequestError: If the request is malformed.
            - NotFoundError: If the rule does not exist.
            - HTTPException: On an unhandled 500 error or if the rule failed.
        """

    def get_log(self):
        """ Get the log.
        ---
        Returns:
            A dictionary with the list of results, where it has rule_name, time and
            result.
        Throws:
            - HTTPException: On an unhandled 500 error.
        """
