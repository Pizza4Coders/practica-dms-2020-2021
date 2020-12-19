""" SensorService class module.
"""

import json
from urllib.parse import urlencode
from http.client import HTTPConnection, HTTPResponse, HTTPException
from dms2021client.data.rest.exc import BadRequestError, ConflictError, NotFoundError
from dms2021client.data.rest.exc import UnauthorizedError


class SensorsService():
    """ REST client to connect to the sensor service.
    """

    def __init__(self, host: str, port: int):
        """ Constructor method.

        Initializes the client.
        ---
        Parameters:
            - host: The sensor service host string.
            - port: The sensor service port number.
        """
        self.__host: str = host
        self.__port: int = port

    def __get_connection(self) -> HTTPConnection:
        """ Creates a new connection to the sensor server.
        ---
        Returns:
            The connection object.
        """
        return HTTPConnection(self.__host, self.__port)

    def is_running(self) -> bool:
        """ Tests whether the sensor service is running or not.
        ---
        Returns:
            True if the sensor service could be contacted successfully; false otherwise.
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

    def get_all_rules(self, user: str) -> List[dict]:
        """ Gets the list of rules.
        ---
        Parameters:
            - user: The username string.
        Returns:
            A dictionary with the list of rules, where each has rule_name, type,
            data and frequency
        Throws:
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': user})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('GET', '/rules/', form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            response_data_json = response.read()
            return json.loads(response_data_json)
        if response.status == 401:
            raise UnauthorizedError()
        if response.status == 500:
            raise HTTPException('Server error')
        return {}

    def get_rule(self, rulename: str, user: str) -> dict:
        """ Gets the specified rule.
        ---
        Parameters:
            - rulename: The rule name string.
            - user: The username string.
        Returns:
            A dictionary with a rule, where it has rule_name, type,
            data and frequency
        Throws:
            - BadRequestError: If the request is malformed.
            - NotFoundError: If the rule does not exist.
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': user})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('GET', '/rule/'+str(rulename), form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            response_data_json = response.read()
            return json.loads(response_data_json)
        if response.status == 400:
            raise BadRequestError()
        if response.status == 401:
            raise UnauthorizedError()
        if response.status == 404:
            raise NotFoundError()
        if response.status == 500:
            raise HTTPException('Server error')
        return {}

    def create_rule(self, rulename: str, ruletype: str, ruleargs: str, frequency: int,
    user: str):
        """ Creates a new rule.
        ---
        Parameters:
            - rulename: The rule name string.
            - ruletype: The type of the rule string. (text: command, file)
            - ruleargs: A command or a file path.
            - frequency (seconds): 0 if it does not execute automatically.
            - user: The username string.
        Throws:
            - BadRequestError: If the request is malformed.
            - ConflictError: If the rule already exists.
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'rulename': rulename, 'ruletype': ruletype,
        'ruleargs': ruleargs, 'frequency': frequency, 'username': user})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('POST', '/rule/', form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            return
        if response.status == 400:
            raise BadRequestError()
        if response.status == 401:
            raise UnauthorizedError()
        if response.status == 409:
            raise ConflictError()
        if response.status == 500:
            raise HTTPException('Server error')

    def delete_rule(self, rulename: str, user: str):
        """ Removes a specified rule.
        ---
        Parameters:
            - rulename: The rule name string.
            - user: The username string.
        Throws:
            - BadRequestError: If the request is malformed.
            - NotFoundError: If the rule does not exist.
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': user})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('DELETE', '/rule/'+str(rulename), form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            return
        if response.status == 400:
            raise BadRequestError()
        if response.status == 401:
            raise UnauthorizedError()
        if response.status == 404:
            raise NotFoundError()
        if response.status == 500:
            raise HTTPException('Server error')

    def run_rule(self, rulename: str, user: str) -> List[dict]:
        """ Runs a specified rule.
        ---
        Parameters:
            - rulename: The rule name string.
            - user: The username string.
        Returns:
            A dictionary with the output (str).
        Throws:
            - BadRequestError: If the request is malformed.
            - NotFoundError: If the rule does not exist.
            - HTTPException: On an unhandled 500 error or if the rule failed.
        """
        form: str = urlencode({'username': user})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('GET', '/rule/' + str(rulename) + '/run/', form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            response_data_json = response.read()
            return json.loads(response_data_json)
        if response.status == 400:
            raise BadRequestError()
        if response.status == 401:
            raise UnauthorizedError()
        if response.status == 404:
            raise NotFoundError()
        if response.status == 500:
            raise HTTPException('Server error')
        return {}

    def get_log(self, user: str) -> dict:
        """ Gets the log.
        ---
        Parameters:
            - user: The username string.
        Returns:
            A dictionary with the list of results, where it has rule_name, time and
            result.
        Throws:
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': user})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('GET', '/log/', form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            response_data_json = response.read()
            return json.loads(response_data_json)
        if response.status == 401:
            raise UnauthorizedError()
        if response.status == 500:
            raise HTTPException('Server error')
        return {}
