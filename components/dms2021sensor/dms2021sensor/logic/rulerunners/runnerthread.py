""" RunnerThread class module.
"""

from threading import Thread
from typing import List
from datetime import datetime
import time
from dms2021sensor.logic import RuleManager, LogManager
from dms2021sensor.data.db.results import Rule

class RunnerThread(Thread):
    """ Background thread that runs rules automatically and logs results
    """
    def set_up(self, rule_manager: RuleManager, log_manager: LogManager):
        """ Sets up the objects for the thread
        """
        self.rule_manager = rule_manager
        self.log_manager = log_manager
        self.rules: List[Rule] = []
        self.rule_manager.create_rule("Archivo file.txt", "file", "/tmp/sensor-volume/file.txt", 30)
        self.rule_manager.create_rule("Estado memoria", "command", "free -m", 30)
        self.rule_manager.create_rule("Uso CPU", "command",
        "mpstat | grep -A 5 \"%idle\" | tail -n 1 | awk -F " " '{print 100 -  $ 12}'a", 30)
        self.rule_manager.create_rule("Info kernel", "command", "uname -a", 0)

    def run(self):
        """ Runs the thread
        """
        print("b")

        last_runs = {}
        self.update_rule_list()
        counter = 0
        while True:
            print("e")
            for rule in self.rules:
                if rule.rule_name not in last_runs:
                    last_runs[rule.rule_name] = datetime.now()
                    self.rule_manager.run_rule(rule.rule_name, self.log_manager)
                else:
                    difference = last_runs[rule.rule_name] - datetime.now()
                    if difference.total_seconds() > rule.frequency:
                        self.rule_manager.run_rule(rule.rule_name, self.log_manager)
            time.sleep(1)
            counter += 1
            if counter >= 14:
                self.update_rule_list()

    def update_rule_list(self):
        """ Updates the rule list
        """
        self.rules = self.rule_manager.get_all_rules()
