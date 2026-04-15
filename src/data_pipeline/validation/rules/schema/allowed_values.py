import pandas as pd
from data_pipeline.validation.result import ValidationResult
from data_pipeline.validation.rules.base import ValidationRule, register_rule


@register_rule("allowed_values")
class AllowedValuesRule(ValidationRule):

    def __init__(self, schema: dict[str, list], severity: str = "error") -> None:
        super().__init__(severity)
        self._schema = schema

    def validate(self, data: pd.DataFrame):

        errors: list[str] = []
        invalid_indices: list[int] = []

        for column, allowed in self._schema.items():

            if column not in data.columns:
                continue

            mask = ~data[column].isin(allowed) & data[column].notna()

            if mask.any():
                invalid_values = set(data.loc[mask, column].unique())
                errors.append(
                    f"Columna '{column}' contiene valores no permitidos: {invalid_values}"
                )
                invalid_indices.extend(self._get_invalid_indices(mask))

        if errors:
            return ValidationResult(
                rule_name=self.__class__.__name__,
                is_valid=False,
                errors=errors,
                severity=self._severity,
                invalid_rows=invalid_indices
            )

        return ValidationResult(
            rule_name=self.__class__.__name__,
            is_valid=True,
            errors=[],
            severity=self._severity,
            invalid_rows=[]
        )
