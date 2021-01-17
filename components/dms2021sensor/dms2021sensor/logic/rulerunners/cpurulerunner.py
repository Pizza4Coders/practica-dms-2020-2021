""" Base rule runner module
"""

from dms2021sensor.data.db.results import Rule
from dms2021sensor.logic.rulerunners.baserulerunner import BaseRuleRunner
from dms2021sensor.logic.rulerunners.exc import RuleRunError
import psutil #type: ignore

class CPURuleRunner(BaseRuleRunner):
    """ Rule runner when type is "cpu".
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
            if rule.data == "all":
                return psutil.cpu_percent(0.5)
            num_core = int(rule.data)
            cpu_loads = psutil.cpu_percent(0.5, True)
            return cpu_loads[num_core]
        except Exception as ex:
            raise RuleRunError from ex
