""" Log class module.
"""

from datetime import datetime
from sqlalchemy import Table, MetaData, Column, String, DateTime # type: ignore
from .resultbase import ResultBase

class Log(ResultBase):
    """ Definition and storage of log ORM records.
    """

    def __init__(self, rule_name: str, time: datetime, result: str):
        """ Constructor method.

        Initializes a rule log.
        ---
        Parameters:
            - rule_name: A string with the rule name.
            - time: A string with the time of the log.
            - result: Either a boolean or a string with the result of the log.
        """
        self.rule_name: str = rule_name
        self.time: datetime = time
        self.result: str = result

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
            Column("time", DateTime, primary_key=True),
            Column("result", String(8192), nullable=False)
        )
