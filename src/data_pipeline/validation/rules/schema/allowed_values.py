import pandas as pd
from data_pipeline.validation.result import ValidationResult
from data_pipeline.validation.rules.base import ValidationRule, register_rule


@register_rule("allowed_values")
class AllowedValuesRule(ValidationRule):
    """
    Valida que los valores de una columna pertenezcan
    a un conjunto permitido definido en el schema.
    """

    def __init__(self, schema: dict[str, list], severity: str = "error") -> None:
        super().__init__(severity)
        self._schema = schema

    def validate(self, data: pd.DataFrame):

        errors: list[str] = []

        for column, allowed in self._schema.items():

            if column not in data.columns:
                continue  # required_columns lo valida

            invalid_values = set(data[column].dropna().unique()) - set(allowed)

            if invalid_values:
                errors.append(
                    f"Columna '{column}' contiene valores no permitidos: {invalid_values}"
                )

        if errors:
            return ValidationResult(
                rule_name=self.__class__.__name__,
                is_valid=False,
                errors=errors,
                severity=self._severity
            )

        return ValidationResult(
            rule_name=self.__class__.__name__,
            is_valid=True,
            errors=[],
            severity=self._severity
        )
