import pandas as pd
from data_pipeline.validation.result import ValidationResult
from data_pipeline.validation.rules.rule_factory import create_rules
from data_pipeline.validation.validation_report import ValidationReport


class RuleEngine:

    def __init__(self, rules_config: list[dict]):
        self._rules = create_rules(rules_config)

    def run(self, data: pd.DataFrame) -> ValidationReport:

        report = ValidationReport()

        for rule in self._rules:

            result: ValidationResult = rule.validate(data)

            report.add(result)

        return report
