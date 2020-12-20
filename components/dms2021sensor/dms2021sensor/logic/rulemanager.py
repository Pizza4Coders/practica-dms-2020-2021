""" RuleManager class module.
"""

from typing import List
from datetime import datetime
from dms2021sensor.data.db.resultsets import Rules
from dms2021sensor.data.db.results import Rule
from dms2021sensor.logic.managerbase import ManagerBase
from dms2021sensor.logic import LogManager
from dms2021sensor.logic.rulerunners import CommandRuleRunner, FileRuleRunner
from dms2021sensor.data.db.exc import RuleNotExistsError

class RuleManager(ManagerBase):
    """ Class responsible of the rule management logic.
    """
    def create_rule(self, rule_name: str, rule_type: str, data: str, frequency: int) -> None:
        """ Creates a new rule
        ---
        Parameters:
            - rule_name: The rule name.
            - rule_type: A string with the type of rule.
            - data: The argument for the rule. A command or a path to a file.
            - frequency: Time in seconds between automatic runs. 0 to disable.
        Throws:
            - ValueError if any of the parameters is missing.
            - RuleExistsError if a rule already exists.
        """
        if not rule_name:
            raise ValueError("A non-empty rule name is needed.")
        if rule_type not in ["file", "command"]:
            raise ValueError("The rule type must be exactly \"file\" or \"command\".")
        if not data:
            raise ValueError("An argument is required")
        session = self.get_schema().new_session()
        Rules.create(session, rule_name, rule_type, data, frequency)

    def rule_exists(self, rule_name: str) -> bool:
        """ Checks if a rule exists
        ---
        Parameters:
            - rule_name: The rule name.
        Returns:
            True if the rule exists, false if not.
        Throws:
            - ValueError if the rule name is missing.
        """
        if not rule_name:
            raise ValueError("The rule name must not be empty.")
        session = self.get_schema().new_session
        return Rules.rule_exists(session, rule_name)

    def get_rule(self, rule_name: str) -> Rule:
        """ Gets a rule
        ---
        Parameters:
            - rule_name: The rule name.
        Returns:
            A Rule object with the rule.
        Throws:
            - ValueError if the rule name is missing.
            - RuleNotExistsError if the rule does not exist.
        """
        if not rule_name:
            raise ValueError("The rule name must not be empty.")
        session = self.get_schema().new_session()
        return Rules.get_rule(session, rule_name)

    def delete_rule(self, rule_name: str) -> bool:
        """ Deletes a rule.
        ---
        Parameters:
            - rule_name: The rule name.
        Returns:
            True if the rule was deleted.
        Throws:
            - ValueError if the rule name is missing.
            - RuleNotExistsError if the rule does not exist.
        """
        if not rule_name:
            raise ValueError("The rule name must not be empty.")
        session = self.get_schema().new_session()
        return Rules.delete_rule(session, rule_name)

    def get_all_rules(self) -> List[Rule]:
        """ Gets all rules
        ---
        Returns:
            A list with all the rules.
        """
        session = self.get_schema().new_session()
        return Rules.get_all_rules(session)

    def run_rule(self, rule_name: str, log_manager: LogManager) -> str:
        """ Runs a rule and logs its results
        ---
        Parameters:
            - rule_name: A string with the rule name.
            - log_manager: A instance of the LogManager
        Returns:
            A string with the result of the action.
        Throws:
            - ValueError if a parameter is missing.
            - RuleNotExistsError if the rule does not exist.
            - LogExistsError if a log already exists
        """
        rule = self.get_rule(rule_name)
        if rule.type == "command":
            result = CommandRuleRunner.run_rule(rule)
            log_manager.create_log(rule_name, datetime.now(), result)
            return result
        if rule.type == "file":
            result = str(FileRuleRunner.run_rule(rule))
            log_manager.create_log(rule_name, datetime.now(), result)
            return result
        raise RuleNotExistsError
