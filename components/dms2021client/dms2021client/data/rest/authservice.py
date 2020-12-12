""" AuthService class module.
"""

import json
from urllib.parse import urlencode
from http.client import HTTPConnection, HTTPResponse, HTTPException
from dms2021client.data.rest.exc import InvalidCredentialsError, UnauthorizedError


class AuthService():
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

    def login(self, username: str, password: str) -> str:
        """ Logs in a user in the authentication server.
        ---
        Parameters:
            - username: The user name string.
            - password: The user password string.
        Returns:
            The session id string.
        Throws:
            - InvalidCredentialsError: If the credentials provided are not correct.
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': username, 'password': password})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('POST', '/sessions', form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            response_data_json = response.read()
            response_data = json.loads(response_data_json)
            return response_data['session_id']
        if response.status == 401:
            raise InvalidCredentialsError()
        if response.status == 500:
            raise HTTPException('Server error')
        return ''

    def logout(self, session_id: str):
        """ Logs out a user from the authentication server.
        ---
        Parameters:
            - session_id: The session id string.
        Throws:
            - UnauthorizedError: If the provided session is incorrect or closed.
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'session_id': session_id})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('DELETE', '/sessions', form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            return

        if response.status == 401:
            raise UnauthorizedError()
        if response.status == 500:
            raise HTTPException('Server error')

    def create_user(self, username: str, password: str, session_id: str):
        """ Creates a user in the authentication server.
        ---
        Parameters:
            - username: The username string.
            - password: The password string.
            - session_id: The session id string.
        Throws:
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': username, 'password': password, 'session_id': session_id})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('POST', '/users', form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            print('El usuario ha sido creado correctamente')
        if response.status == 400:
            print('Error de sintaxis. Pruebe de nuevo')
        if response.status == 403: # Podría también emplearse el 401
            print('Usted no tiene los permisos para realizar esta operación')
        if response.status == 409:
            print('El usuario que intenta crear ya existe')
        if response.status == 500:
            print('Error inesperado')
            raise HTTPException('Server error')

    def grant(self, username: str, right: str, session_id: str):
        """ Grant a right to a user from the authentication server.
        ---
        Parameters:
            - username: The username string.
            - right: The right string.
            - session_id: The session id string.
        Throws:
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': username, 'right': right, 'session_id': session_id})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('POST', '/users/'+str(username)+'/rights'+str(right), form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            print('Permiso otorgado correctamente')
        if response.status == 400:
            print('Error de sintaxis. Pruebe de nuevo')
        if response.status == 403: # Podría también emplearse el 401
            print('Usted no tiene los permisos para realizar esta operación')
        if response.status == 500:
            print('Error inesperado')
            raise HTTPException('Server error')

    def revoke(self, username: str, right: str, session_id: str):
        """ Revoke a right to a user from the authentication server.
        ---
        Parameters:
            - username: The username string.
            - right: The right string.
            - session_id: The session id string.
        Throws:
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': username, 'right': right, 'session_id': session_id})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('DELETE', '/users/'+str(username)+'/rights'+str(right), form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            print('Permiso retirado correctamente del usuario')
        if response.status == 400:
            print('Error de sintaxis. Pruebe de nuevo')
        if response.status == 403: # Podría también emplearse el 401
            print('Usted no tiene los permisos para realizar esta operación')
        if response.status == 404:
            print('ERROR 404.')
        if response.status == 500:
            print('Error inesperado')
            raise HTTPException('Server error')

    def has_right(self, username: str, right: str) -> bool:
        """ Determines whether a given user from the authentication server
            has a certain right or not.
        ---
        Parameters:
            - username: The user name string.
            - right: The right name.
        Returns:
            True if the user has the given right; false otherwise.
        Throws:
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': username, 'right': right})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('DELETE', '/users/'+str(username)+'/rights'+str(right), form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            print('Permiso retirado correctamente del usuario')
        if response.status == 400: # REVISAR ESTO
            print('Error de sintaxis. Pruebe de nuevo')
        if response.status == 404:
            print('ERROR 404')
        if response.status == 500:
            print('Error inesperado')
            raise HTTPException('Server error')
        