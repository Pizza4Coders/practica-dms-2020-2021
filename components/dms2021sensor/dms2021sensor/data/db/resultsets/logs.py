""" Logs class module.
"""

from typing import Optional, List
from datetime import datetime
from dms2021sensor.data.db.results.log import Log
from dms2021sensor.data.db.resultsets.rules import Rules
from dms2021sensor.data.db.exc import RuleNotExistsError, LogExistsError, LogNotExistsError
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
        if not rule_name:
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

    @staticmethod
    def get_last_run(session: Session, rule_name: str) -> Log:
        """ Gets the latest log for a rule
        ---
        Parameters:
            - session: The session object.
            - rule_name: The rule name.
        Returns:
            The last log for a rule.
        Throws:
            - LogNotExistsError if there are not any logs for that rule.
            - RuleNotExistsError if the rule does not exist.
        """
        if not Rules.rule_exists(session, rule_name):
            raise RuleNotExistsError
        query = session.query(Log).filter_by(rule_name=rule_name).order_by("time desc")
        log: Optional[Log] = query.first()
        if log is None:
            raise LogNotExistsError
        return log

    @staticmethod
    def get_all_runs(session: Session) -> List[Log]:
        """ Gets all the logs
        ---
        Parameters:
            - session: The session object.
        Returns:
            A list with all the logs.
        """
        query = session.query(Log)
        return query.all()
