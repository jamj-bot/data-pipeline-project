import pandas as pd
from data_pipeline.validation.result import ValidationResult
from data_pipeline.validation.rules.base import ValidationRule, register_rule


@register_rule("value_range")
class ValueRangeRule(ValidationRule):

    def __init__(
        self,
        schema: dict[str, dict],
        severity: str = "error"
    ) -> None:
        super().__init__(severity)
        self._schema = schema

    def validate(self, data: pd.DataFrame):

        errors: list[str] = []
        invalid_indices: list[int] = []

        for column, constraints in self._schema.items():

            if column not in data.columns:
                continue

            series = data[column]

            if series.dropna().empty:
                continue

            min_value = constraints.get("min")
            max_value = constraints.get("max")
            min_inclusive = constraints.get("min_inclusive", True)
            max_inclusive = constraints.get("max_inclusive", True)

            column_mask = pd.Series(False, index=data.index)

            if min_value is not None:
                if min_inclusive:
                    min_mask = series < min_value
                else:
                    min_mask = series <= min_value

                if min_mask.any():
                    errors.append(
                        f"Columna '{column}' contiene valores menores al mínimo permitido ({min_value})"
                    )
                    column_mask = self._combine_masks(column_mask, min_mask)

            if max_value is not None:
                if max_inclusive:
                    max_mask = series > max_value
                else:
                    max_mask = series >= max_value

                if max_mask.any():
                    errors.append(
                        f"Columna '{column}' contiene valores mayores al máximo permitido ({max_value})"
                    )
                    column_mask = self._combine_masks(column_mask, max_mask)

            if column_mask.any():
                invalid_indices.extend(self._get_invalid_indices(column_mask))

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
