""" AuthService class module.
"""

from urllib.parse import urlencode
from http.client import HTTPConnection, HTTPResponse, HTTPException
from dms2021sensor.data.rest.exc import NotFoundError


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

    def has_right(self, username: str, right: str) -> bool:
        """ Determines whether a given user from the authentication server
            has a certain right or not.
        ---
        Parameters:
            - username: The user name string.
            - right: The right name.
        Returns:
            True if the user has the given right
        Throws:
            - NotFoundError: if the user does not have the right, the user does not
              exist, or the right does not exist.
            - HTTPException: On an unhandled 500 error.
        """
        form: str = urlencode({'username': username, 'right': right})
        headers: dict = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        connection: HTTPConnection = self.__get_connection()
        connection.request('GET', '/users/'+str(username)+'/rights/'+str(right), form, headers)
        response: HTTPResponse = connection.getresponse()
        if response.status == 200:
            return True
        if response.status == 404:
            raise NotFoundError()
        if response.status == 500:
            raise HTTPException('Server error')
        return False
