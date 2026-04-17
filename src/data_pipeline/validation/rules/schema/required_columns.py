import pandas as pd
from data_pipeline.validation.result import ValidationResult
from data_pipeline.validation.rules.base import ValidationRule, register_rule


@register_rule("required_columns")
class RequiredColumnsRule(ValidationRule):

    def __init__(self, columns: list[str], severity: str = "error") -> None:
        super().__init__(severity)
        self._columns = columns

    def validate(self, data: pd.DataFrame):

        missing = set(self._columns) - set(data.columns)

        if missing:
            return ValidationResult(
                rule_name=self.__class__.__name__,
                is_valid=False,
                errors=[f"Faltan columnas requeridas: {missing}"],
                severity=self._severity,
                is_row_level=False,
                invalid_rows=[]
            )

        return ValidationResult(
            rule_name=self.__class__.__name__,
            is_valid=True,
            errors=[],
            severity=self._severity,
            is_row_level=False,
            invalid_rows=[]
        )


