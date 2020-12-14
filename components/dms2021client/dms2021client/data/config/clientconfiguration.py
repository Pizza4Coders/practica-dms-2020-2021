""" ClientConfiguration class module.
"""

from dms2021core.data.config import Configuration, ConfigurationValueType
from typing import Dict


class ClientConfiguration(Configuration):
    """ Class responsible of storing a specific client configuration.
    """

    def _component_name(self) -> str:
        """ The component name, to categorize the default config path.
        ---
        Returns:
            A string identifying the component which will categorize the configuration.
        """

        return 'dms2021client'

    def __init__(self):
        """ Initialization/constructor method.
        """

        Configuration.__init__(self)

    def _validate_values(self, values: dict) -> None:
        """ Validates a set of configuration values.

        Subclasses are expected to override this method and provide their own
        domain-specific validation.
        ---
        Parameters:
            - values: The dictionary of configuration values.
        Throws:
            - A `ValueError` exception if validation is not passed.
        """

    def __get_auth_service_value(self) -> dict:
        """ Gets the value of the auth_service configuration dictionary.
        ---
        Returns:
            A dictionary with the authentication service configured parameters.
        """
        auth_service_value: ConfigurationValueType = self.get_value(
            'auth_service'
        )
        if not isinstance(auth_service_value, dict):
            raise TypeError(
                'Configuration parameter auth_service is expected to be a dictionary. Received: '
                + str(type(auth_service_value))
            )
        return auth_service_value

    def __get_sensors_service_value(self) -> dict:
        """ Gets the value of the auth_service configuration dictionary.
        ---
        Returns:
            A dictionary with the authentication service configured parameters.
        """
        sensors_service_value: ConfigurationValueType = self.get_value(
            'sensors'
        )
        if not isinstance(sensors_service_value, dict):
            raise TypeError(
                'Configuration parameter auth_service is expected to be a dictionary. Received: '
                + str(type(sensors_service_value))
            )
        return sensors_service_value

    def get_auth_service_host(self) -> str:
        """ Gets the authentication service host configuration value.
        ---
        Returns:
            A string with the value of authservice host.
        Throws:
            - TypeError: if the authservice parameter is not a dictionary.
        """

        auth_service_value: dict = self.__get_auth_service_value()
        return str(auth_service_value['host'])

    def get_sensor1_service_host(self) -> str:
        """ Gets the authentication service host configuration value.
        ---
        Returns:
            A string with the value of authservice host.
        Throws:
            - TypeError: if the authservice parameter is not a dictionary.
        """

        sensors_service_value: dict = self.__get_sensors_service_value()
        return str(sensors_service_value["sensor1"]['host'])

    def get_sensor2_service_host(self) -> str:
        """ Gets the authentication service host configuration value.
        ---
        Returns:
            A string with the value of authservice host.
        Throws:
            - TypeError: if the authservice parameter is not a dictionary.
        """

        sensors_service_value: dict = self.__get_sensors_service_value()
        return str(sensors_service_value["sensor2"]['host'])

    def get_auth_service_port(self) -> int:
        """ Gets the authentication service port configuration value.
        ---
        Returns:
            An integer with the value of authservice port.
        Throws:
            - TypeError: if the authservice parameter is not a dictionary.
        """

        auth_service_value: dict = self.__get_auth_service_value()
        return int(str(auth_service_value['port']))

    def get_sensor1_service_port(self) -> int:
        """ Gets the authentication service port configuration value.
        ---
        Returns:
            An integer with the value of authservice port.
        Throws:
            - TypeError: if the authservice parameter is not a dictionary.
        """

        sensors_service_value: dict = self.__get_sensors_service_value()
        return int(str(sensors_service_value["sensor1"]['port']))

    def get_sensor2_service_port(self) -> int:
        """ Gets the authentication service port configuration value.
        ---
        Returns:
            An integer with the value of authservice port.
        Throws:
            - TypeError: if the authservice parameter is not a dictionary.
        """

        sensors_service_value: dict = self.__get_sensors_service_value()
        return int(str(sensors_service_value["sensor2"]['port']))

    def get_debug_flag(self) -> bool:
        """ Gets whether the debug flag is set or not.
        ---
        Returns:
            A boolean with the value of debug.
        """

        return bool(self.get_value('debug'))
