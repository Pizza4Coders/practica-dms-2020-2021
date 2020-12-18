""" Base rule runner module
"""

from os.path import isfile
from dms2021sensor.data.db.results import Rule
from dms2021sensor.logic.rulerunners.baserulerunner import BaseRuleRunner
from dms2021sensor.logic.rulerunners.exc import RuleRunError

class FileRuleRunner(BaseRuleRunner):
    """ Rule runner when type is "file".
    """
    @staticmethod
    def run_rule(rule: Rule) -> str:
        """ Runs a rule and returns its result
        ---
        Parameters:
            rule: A rule object
        Returns:
            The result of the rule as a string.
        """
        try:
            return str(isfile(rule.data))
        except Exception as ex:
            raise RuleRunError from ex
