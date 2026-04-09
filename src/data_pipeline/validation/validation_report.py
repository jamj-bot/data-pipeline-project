from dataclasses import dataclass, field
from typing import List
from data_pipeline.validation.result import ValidationResult


@dataclass
class ValidationReport:
    results: List[ValidationResult] = field(default_factory=list)

    def add(self, result: ValidationResult) -> None:
        self.results.append(result)

    @property
    def errors(self) -> List[ValidationResult]:
        return [r for r in self.results if not r.is_valid and r.severity == "error"]

    @property
    def warnings(self) -> List[ValidationResult]:
        return [r for r in self.results if not r.is_valid and r.severity == "warning"]

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def summary(self) -> dict:
        return {
            "total_rules": len(self.results),
            "errors": len(self.errors),
            "warnings": len(self.warnings),
        }

    def to_dict(self) -> dict:
        return {
            "summary": self.summary(),
            "errors": [
                {
                    "rule": e.rule_name,
                    "messages": e.errors,
                    "severity": e.severity,
                }
                for e in self.errors
            ],
            "warnings": [
                {
                    "rule": w.rule_name,
                    "messages": w.errors,
                    "severity": w.severity,
                }
                for w in self.warnings
            ],
        }
