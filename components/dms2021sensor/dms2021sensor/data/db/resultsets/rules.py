""" Rules class module.
"""

from dms2021sensor.data.db.results.rule import Rule
from dms2021sensor.data.db.exc import RuleExistsError
from sqlalchemy.exc import IntegrityError # type: ignore
from sqlalchemy.orm.session import Session # type: ignore
from sqlalchemy.orm.exc import NoResultFound # type: ignore

class Rules():
    """ Class responsible of table-level rules operations
    """
    @staticmethod
    def create(session: Session, rule_name: str, rule_type: str, data: str, frequency: int) -> Rule:
        """ Creates a new rule record.
        ---
        Note:
            Any existing transaction will be committed.
        Parameters:
            - session: The session object.
            - rule_name: The rule name string.
            - rule_type: The string of the rule type.
            - data: The string of the argument of the rule.
            - frequency: The number of seconds after a rule is repeated.
        Returns:
            The created Rule result.
        Throws:
            - ValueError: If some parameter is missing
        """
        if not rule_name or not rule_type or not data or not frequency:
            raise ValueError("A rule name, a type, an argument and a frequency is required.")
        try:
            rule = Rule(rule_name, rule_type, data, frequency)
            session.add(rule)
            session.commit()
            return rule
        except IntegrityError as ex:
            raise RuleExistsError("The rule already exists") from ex

    @staticmethod
    def rule_exists(session: Session, rule_name: str) -> bool:
        """ Checks if a rule exists
        ---
        Parameters:
            - session: The session object.
            - rule_name: The name of a rule.
        Return:
            True if the rule exists, False if not.
        """
        try:
            query = session.query(Rule).filter_by(rule_name=rule_name)
            query.one()
        except NoResultFound:
            return False
        return True
