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
        """ #TODO Document this later
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
        """ #TODO Document this later
        if not rule_name:
            raise ValueError("A rule name is required.")
        session = self.get_schema().new_session()
        return Logs.get_last_run(session, rule_name)

    def get_all_runs(self) -> List[Log]:
        """ Gets all the logs.
        ---
        """ #TODO Document this later
        session = self.get_schema().new_session()
        return Logs.get_all_runs(session)
