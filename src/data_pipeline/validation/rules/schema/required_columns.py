import pandas as pd
from data_pipeline.validation.rules.base import ValidationRule, register_rule

@register_rule("required_columns")
class RequiredColumnsRule(ValidationRule):

    def __init__(self, columns: list[str], severity: str = "error") -> None:
        super().__init__(severity)
        self._columns = columns

    def validate(self, data: pd.DataFrame) -> None:

        missing = set(self._columns) - set(data.columns)

        if missing:
            raise ValueError(f"Faltan columnas requeridas: {missing}")
