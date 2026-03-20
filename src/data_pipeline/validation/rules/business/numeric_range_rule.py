import pandas as pd
from data_pipeline.validation.rules.base import ValidationRule, register_rule


@register_rule("numeric_range")
class NumericRangeRule(ValidationRule):

    def __init__(
        self,
        column: str,
        min: float | None = None,
        max: float | None = None,
        severity: str = "error"
    ) -> None:
        super().__init__(severity)
        self._column = column
        self._min = min
        self._max = max

    def validate(self, data: pd.DataFrame) -> None:

        if self._column not in data.columns:
            return

        series = data[self._column]

        if self._min is not None:
            if (series < self._min).any():
                raise ValueError(
                    f"{self._column} contiene valores menores que {self._min}"
                )

        if self._max is not None:
            if (series > self._max).any():
                raise ValueError(
                    f"{self._column} contiene valores mayores que {self._max}"
                )
