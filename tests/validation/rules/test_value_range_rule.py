# tests/validation/rules/test_value_range_rule.py
import pytest
import pandas as pd
from data_pipeline.validation.rules.schema.value_range import ValueRangeRule


class TestValueRangeRule:
    """Tests para ValueRangeRule."""

    def test_all_values_in_range(self, sample_df_numeric):
        """Todos los valores dentro de rango."""
        schema = {
            "price": {"min": 5, "max": 60},
            "quantity": {"min": 0, "max": 30}
        }
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(sample_df_numeric)
        
        assert result.is_valid is True

    def test_values_below_minimum(self):
        """Valores por debajo del mínimo."""
        df = pd.DataFrame({"age": [5, 15, 25, 35]})
        schema = {"age": {"min": 18}}
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is False
        assert set(result.invalid_rows) == {0, 1}

    def test_values_above_maximum(self):
        """Valores por encima del máximo."""
        df = pd.DataFrame({"age": [15, 25, 35, 45, 55]})
        schema = {"age": {"max": 40}}
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is False
        assert set(result.invalid_rows) == {3, 4}

    def test_min_and_max(self):
        """Rango con mín y máx."""
        df = pd.DataFrame({"score": [0, 50, 100, 150]})
        schema = {"score": {"min": 0, "max": 100}}
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is False
        assert result.invalid_rows == [3]

    def test_inclusive_boundaries(self):
        """Límites inclusivos (por defecto)."""
        df = pd.DataFrame({"value": [10, 20, 30]})
        schema = {
            "value": {
                "min": 10,
                "max": 30,
                "min_inclusive": True,
                "max_inclusive": True
            }
        }
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is True

    def test_exclusive_boundaries(self):
        """Límites exclusivos."""
        df = pd.DataFrame({"value": [10, 20, 30]})
        schema = {
            "value": {
                "min": 10,
                "max": 30,
                "min_inclusive": False,
                "max_inclusive": False
            }
        }
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is False
        assert set(result.invalid_rows) == {0, 2}

    def test_null_values_ignored(self):
        """Los valores nulos se ignoran."""
        df = pd.DataFrame({"age": [10, None, 30, None, 50]})
        schema = {"age": {"min": 0, "max": 40}}
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is False
        assert result.invalid_rows == [4]  # Solo 50 es inválido

    def test_missing_column_ignored(self, sample_df_numeric):
        """Columnas no presentes se ignoran."""
        schema = {
            "nonexistent": {"min": 0, "max": 100},
            "price": {"min": 0, "max": 100}
        }
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(sample_df_numeric)
        
        assert result.is_valid is True

    def test_is_row_level_true(self):
        """Esta es una regla row-level."""
        df = pd.DataFrame({"value": [10, 50]})
        schema = {"value": {"min": 0, "max": 40}}
        rule = ValueRangeRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_row_level is True
        assert result.invalid_rows == [1]
