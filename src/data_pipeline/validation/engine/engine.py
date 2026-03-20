import pandas as pd
from data_pipeline.validation.rules.rule_factory import create_rules


class RuleEngine:

    def __init__(self, rules_config: list[dict]):
        self._rules = create_rules(rules_config)

    def run(self, data: pd.DataFrame) -> None:

        for rule in self._rules:
            try:
                rule.validate(data)
            except Exception as e:
                if getattr(rule, "_severity", "error") == "warning":
                    print(f"WARNING: {e}")
                else:
                    raise


