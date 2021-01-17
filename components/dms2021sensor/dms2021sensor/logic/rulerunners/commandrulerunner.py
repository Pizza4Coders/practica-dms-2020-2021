""" Base rule runner module
"""

import subprocess
from dms2021sensor.data.db.results import Rule
from dms2021sensor.logic.rulerunners.baserulerunner import BaseRuleRunner
from dms2021sensor.logic.rulerunners.exc import RuleRunError

class CommandRuleRunner(BaseRuleRunner):
    """ Rule runner when type is "command".
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
            result = subprocess.run(rule.data, stdout=subprocess.PIPE, check=True, shell=True)
            return result.stdout.decode("utf-8")
        except subprocess.CalledProcessError as ex:
            raise RuleRunError from ex
