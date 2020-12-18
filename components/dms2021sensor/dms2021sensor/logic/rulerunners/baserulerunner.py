""" Base rule runner module
"""

from abc import ABC, abstractmethod
from dms2021sensor.data.db.results import Rule

class BaseRuleRunner(ABC):
    """ A base class for the rule runners.
    """
    @abstractmethod
    @staticmethod
    def run_rule(rule: Rule) -> str:
        """ Runs a rule and returns its result
        ---
        Parameters:
            rule: A rule object
        Returns:
            The result of the rule as a string.
        """
