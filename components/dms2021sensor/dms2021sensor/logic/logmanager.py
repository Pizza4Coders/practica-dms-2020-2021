""" LogManager class module.
"""

from typing import List
from datetime import datetime
from dms2021sensor.data.db.resultsets import Logs
from dms2021sensor.data.db.results import Log
from dms2021sensor.logic.managerbase import ManagerBase


class LogManager(ManagerBase):
    """ Class responsible of the log management logic.
    """
    def create_log(self, rule_name: str, time: datetime, result: str) -> None:
        """ Creates a new log
        ---
        Parameters:
            - rule_name: The rule name
            - time: A datetime.
            - result: A string with the result.
        Throws:
            - ValueError if any of the parameters is missing.
            - RuleNotExistsError if the rule does not exist.
            - LogExistsError if a log already exists.
        """
        if not rule_name:
            raise ValueError("A rule name is required.")
        if not time:
            raise ValueError("A datetime is required.")
        if not result:
            raise ValueError("A result is required.")
        session = self.get_schema().new_session()
        Logs.create(session, rule_name, time, result)

    def get_last_run(self, rule_name: str) -> Log:
        """ Gets the last log for a rule.
        ---
        Parameters:
            - rule_name: The rule name.
        Returns:
            A Log object with the last rule run.
        Throws:
            - ValueError if the rule name is missing.
            - RuleNotExistsError if the rule does not exist.
            - LogNotExistsError if there is no log record for that rule.
        """
        if not rule_name:
            raise ValueError("A rule name is required.")
        session = self.get_schema().new_session()
        return Logs.get_last_run(session, rule_name)

    def get_all_runs(self) -> List[Log]:
        """ Gets all the logs.
        ---
        Returns:
            A list with all of the logs that exists on the system.
        """
        session = self.get_schema().new_session()
        return Logs.get_all_runs(session)
