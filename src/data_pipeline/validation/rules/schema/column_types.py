import pandas as pd
from data_pipeline.validation.result import ValidationResult
from pandas.api.types import is_dtype_equal
from data_pipeline.validation.rules.base import ValidationRule, register_rule


@register_rule("column_types")
class ColumnTypesRule(ValidationRule):

    _TYPE_MAPPING: dict[str, object] = {
        "int": "int64",
        "Int8": pd.Int8Dtype(),
        "Int16": pd.Int16Dtype(),
        "Int32": pd.Int32Dtype(),
        "Int64": pd.Int64Dtype(),
        "float": "float64",
        "Float32": pd.Float32Dtype(),
        "Float64": pd.Float64Dtype(),
        "bool": "bool",
        "boolean": pd.BooleanDtype(),
        "string": pd.StringDtype(),
        "datetime": "datetime64[ns]",
        "timedelta": "timedelta64[ns]",
    }

    def __init__(self, schema: dict[str, str], severity: str = "error") -> None:
        super().__init__(severity)
        self._schema = schema

    def validate(self, data: pd.DataFrame):

        errors: list[str] = []

        for column, declared_type in self._schema.items():

            if column not in data.columns:
                continue

            expected_dtype = self._TYPE_MAPPING.get(declared_type)

            if expected_dtype is None:
                return ValidationResult(
                    rule_name=self.__class__.__name__,
                    is_valid=False,
                    errors=[f"Tipo no soportado en column_types: '{declared_type}'"],
                    severity=self._severity,
                    is_row_level=False,
                    invalid_rows=[]
                )

            actual_dtype = data[column].dtype

            if not is_dtype_equal(actual_dtype, expected_dtype):
                errors.append(
                    f"Columna '{column}' dtype actual '{actual_dtype}' "
                    f"≠ esperado '{declared_type}'"
                )

        if errors:
            return ValidationResult(
                rule_name=self.__class__.__name__,
                is_valid=False,
                errors=errors,
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
