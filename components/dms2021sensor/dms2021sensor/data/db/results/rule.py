""" Rule class module
"""

from typing import Dict
from sqlalchemy import Table, MetaData, Column, String, Integer # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from dms2021sensor.data.db.results.log import Log
from .resultbase import ResultBase

class Rule(ResultBase):
    """ Definition and storage of rule ORM records.
    """

    def __init__(self, rule_name: str, rule_type: str, data: str, frequency: int):
        """ Constructor method.

        Initializes a rule.
        ---
        Parameters:
            - rule_name: A string with the rule name.
            - time: A string with the time of the log.
            - result: Either a boolean or a string with the result of the log.
        """
        self.rule_name: str = rule_name
        self.type: str = rule_type
        self.data: str = data
        self.frequency: int = frequency

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.
        ---
        Parameters:
            - metadata: The database schema metadata
        Returns:
            A Table object with the table definition.
        """
        return Table(
            "logs",
            metadata,
            Column("rule_name", String(32), primary_key=True),
            Column("type", String(32), nullable=False),
            Column("data", String(1024), nullable=False),
            Column("frequency", Integer, nullable=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        """ Gets the mapping properties dictionary.
        ---
        Returns:
            A dictionary with the mapping properties.
        """
        return{
            "logs": relationship(Log, backref="rule")
        }

    def __str__(self) -> str:
        """ Gets the object as a string.
        ---
        Returns:
            The object formatted as a json-formatted string.
        """
        return str({
            "rule_name": self.rule_name,
            "type": self.type,
            "data": self.data,
            "frequency": self.frequency
        })
