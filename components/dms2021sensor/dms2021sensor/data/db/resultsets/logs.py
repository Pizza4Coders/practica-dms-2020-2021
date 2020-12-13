""" Logs class module.
"""

from datetime import datetime
from dms2021sensor.data.db.results.log import Log
from dms2021sensor.data.db.resultsets.rules import Rules
from dms2021sensor.data.db.exc import RuleNotExistsError, LogExistsError
from sqlalchemy.exc import IntegrityError # type: ignore
from sqlalchemy.orm.session import Session # type: ignore


class Logs():
    """ Class responsible of table-level logs operations
    """
    @staticmethod
    def create(session: Session, rule_name: str, time: datetime, result: str) -> Log:
        """ Creates a new log record.
        ---
        Note:
            Any existing transaction will be committed.
        Parameters:
            - session: The session object.
            - rule_name: The rule name string.
            - time: The date time of the log.
            - result: The result.
        Returns:
            The created Log result.
        Throws:
            - RuleNotExistsError: If the rule doesn't exist.
            - ValueError: If the rule_name, time or result is missing.
            - LogExistsError: If the Log already exists.
        """
        if not rule_name or not time or not result:
            raise ValueError("A rule name, a time and a result is required.")
        try:
            if not Rules.rule_exists(session, rule_name):
                raise RuleNotExistsError("The specified rule does not exist.")
            log = Log(rule_name, time, result)
            session.add(log)
            session.commit()
            return log
        except IntegrityError as ex:
            raise LogExistsError("The log already exists") from ex

# TO-DO Get logs
