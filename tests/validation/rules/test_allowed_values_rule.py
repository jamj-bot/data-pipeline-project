# tests/validation/rules/test_allowed_values_rule.py
import pytest
import pandas as pd
from data_pipeline.validation.rules.schema.allowed_values import AllowedValuesRule


class TestAllowedValuesRule:
    """Tests para AllowedValuesRule."""

    def test_all_values_allowed(self, sample_df_categories):
        """Todos los valores son permitidos."""
        schema = {
            "status": ["active", "inactive", "pending"],
            "region": ["US", "EU", "ASIA"]
        }
        rule = AllowedValuesRule(schema=schema)
        result = rule.validate(sample_df_categories)
        
        assert result.is_valid is True
        assert result.errors == []

    def test_some_values_not_allowed(self):
        """Algunos valores no están permitidos."""
        df = pd.DataFrame({
            "status": ["active", "inactive", "unknown"]
        })
        
        schema = {"status": ["active", "inactive"]}
        rule = AllowedValuesRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "unknown" in str(result.errors[0])

    def test_invalid_rows_identified(self):
        """Se identifican las filas inválidas."""
        df = pd.DataFrame({
            "status": ["active", "invalid", "active", "invalid"]
        })
        
        schema = {"status": ["active"]}
        rule = AllowedValuesRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is False
        assert set(result.invalid_rows) == {1, 3}

    def test_null_values_allowed(self):
        """Los valores nulos no se consideran inválidos."""
        df = pd.DataFrame({
            "status": ["active", None, "inactive"]
        })
        
        schema = {"status": ["active", "inactive"]}
        rule = AllowedValuesRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is True

    def test_missing_column_ignored(self, sample_df_categories):
        """Columnas no presentes se ignoran."""
        schema = {
            "nonexistent": ["value1", "value2"],
            "status": ["active", "inactive", "pending"]
        }
        rule = AllowedValuesRule(schema=schema)
        result = rule.validate(sample_df_categories)
        
        assert result.is_valid is True

    def test_is_row_level_true(self):
        """Esta es una regla row-level."""
        df = pd.DataFrame({"status": ["active", "invalid"]})
        schema = {"status": ["active"]}
        rule = AllowedValuesRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_row_level is True

    def test_multiple_columns_multiple_errors(self):
        """Errores en múltiples columnas."""
        df = pd.DataFrame({
            "col1": ["a", "b", "invalid"],
            "col2": ["x", "invalid", "z"]
        })
        
        schema = {
            "col1": ["a", "b"],
            "col2": ["x", "z"]
        }
        rule = AllowedValuesRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is False
        assert len(result.errors) == 2

    def test_severity_warning(self):
        """Severidad warning."""
        df = pd.DataFrame({"status": ["invalid"]})
        schema = {"status": ["active"]}
        rule = AllowedValuesRule(schema=schema, severity="warning")
        result = rule.validate(df)
        
        assert result.severity == "warning"
