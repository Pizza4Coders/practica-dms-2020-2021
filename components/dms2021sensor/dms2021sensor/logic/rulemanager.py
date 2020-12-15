""" UserManager class module.
"""

from dms2021sensor.data.db.resultsets import Rules
from dms2021sensor.logic.managerbase import ManagerBase


class RuleManager(ManagerBase):
    """ Class responsible of the rule management logic.
    """
    def create_rule(self, rule_name: str, rule_type: str, data: str, frequency: int) -> None:
        """ Creates a new rule
        ---
        """ #TODO Documentar después
        if not rule_name:
            raise ValueError("A non-empty rule name is needed.")
        if rule_type not in ["file", "command"]:
            raise ValueError("The rule type must be exactly \"file\" or \"command\".")
        if not data:
            raise ValueError("An argument is required")
        session = self.get_schema().new_session()
        Rules.create(session, rule_name, rule_type, data, frequency)
