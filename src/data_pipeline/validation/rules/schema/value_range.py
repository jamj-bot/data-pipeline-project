import pandas as pd
from data_pipeline.validation.result import ValidationResult
from data_pipeline.validation.rules.base import ValidationRule, register_rule


@register_rule("value_range")
class ValueRangeRule(ValidationRule):
    """
    Valida que los valores de una columna estén dentro de un rango definido.
    Aplica a tipos numéricos o temporales.
    No muta datos.
    """

    def __init__(
        self,
        schema: dict[str, dict],
        severity: str = "error"
    ) -> None:
        """
        schema ejemplo:
        {
            "DEP_DELAY": {"min": -60, "max": 600},
            "PERCENTAGE": {"min": 0, "max": 100},
            "DURATION": {"min": "0 days"}
        }
        """
        super().__init__(severity)
        self._schema = schema

    def validate(self, data: pd.DataFrame):

        errors: list[str] = []

        for column, constraints in self._schema.items():

            if column not in data.columns:
                continue

            series = data[column].dropna()

            if series.empty:
                continue

            min_value = constraints.get("min")
            max_value = constraints.get("max")
            min_inclusive = constraints.get("min_inclusive", True)
            max_inclusive = constraints.get("max_inclusive", True)

            # Comparación mínima
            if min_value is not None:
                if min_inclusive:
                    invalid = series[series < min_value]
                else:
                    invalid = series[series <= min_value]

                if not invalid.empty:
                    errors.append(
                        f"Columna '{column}' contiene valores menores al mínimo permitido ({min_value})"
                    )

            # Comparación máxima
            if max_value is not None:
                if max_inclusive:
                    invalid = series[series > max_value]
                else:
                    invalid = series[series >= max_value]

                if not invalid.empty:
                    errors.append(
                        f"Columna '{column}' contiene valores mayores al máximo permitido ({max_value})"
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
