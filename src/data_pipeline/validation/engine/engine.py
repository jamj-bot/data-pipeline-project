import pandas as pd
from data_pipeline.validation.result import ValidationResult
from data_pipeline.validation.rules.rule_factory import create_rules


class RuleEngine:

    def __init__(self, rules_config: list[dict]):
        self._rules = create_rules(rules_config)

    def run(self, data: pd.DataFrame) -> None:

        for rule in self._rules:
            try:
                result = rule.validate(data)

                # NUEVO: soporte para ValidationResult
                if isinstance(result, ValidationResult):

                    if not result.is_valid:
                        if result.severity == "warning":
                            print(f"WARNING [{result.rule_name}]: {result.errors}")
                        else:
                            raise ValueError(
                                f"ERROR [{result.rule_name}]: {result.errors}"
                            )

            except Exception as e:
                # comportamiento legacy (no se rompe nada)
                if getattr(rule, "_severity", "error") == "warning":
                    print(f"WARNING: {e}")
                else:
                    raise


