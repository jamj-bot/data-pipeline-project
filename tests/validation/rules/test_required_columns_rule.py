# tests/validation/rules/test_required_columns_rule.py
import pytest
import pandas as pd
from data_pipeline.validation.rules.schema.required_columns import RequiredColumnsRule


class TestRequiredColumnsRule:
    """Tests para RequiredColumnsRule."""

    def test_all_columns_present(self, sample_df):
        """Todas las columnas requeridas existen."""
        rule = RequiredColumnsRule(columns=["id", "name", "age"])
        result = rule.validate(sample_df)
        
        assert result.is_valid is True
        assert result.errors == []
        assert result.is_row_level is False

    def test_missing_single_column(self, sample_df):
        """Falta una columna."""
        rule = RequiredColumnsRule(columns=["id", "name", "nonexistent"])
        result = rule.validate(sample_df)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "nonexistent" in result.errors[0]

    def test_missing_multiple_columns(self, sample_df):
        """Faltan múltiples columnas."""
        rule = RequiredColumnsRule(columns=["id", "col1", "col2", "col3"])
        result = rule.validate(sample_df)
        
        assert result.is_valid is False
        assert len(result.errors) == 1

    def test_empty_dataframe(self):
        """DataFrame vacío."""
        df = pd.DataFrame()
        rule = RequiredColumnsRule(columns=["id", "name"])
        result = rule.validate(df)
        
        assert result.is_valid is False

    def test_no_required_columns(self, sample_df):
        """Sin columnas requeridas."""
        rule = RequiredColumnsRule(columns=[])
        result = rule.validate(sample_df)
        
        assert result.is_valid is True

    def test_case_sensitive(self, sample_df):
        """Las columnas son case-sensitive."""
        rule = RequiredColumnsRule(columns=["ID"])  # uppercase
        result = rule.validate(sample_df)
        
        assert result.is_valid is False  # 'ID' != 'id'

    def test_invalid_rows_always_empty(self, sample_df):
        """Las reglas estructurales nunca tienen filas inválidas."""
        rule = RequiredColumnsRule(columns=["nonexistent"])
        result = rule.validate(sample_df)
        
        assert result.invalid_rows == []

    def test_severity_error(self, sample_df):
        """Severidad error por defecto."""
        rule = RequiredColumnsRule(columns=["nonexistent"], severity="error")
        result = rule.validate(sample_df)
        
        assert result.severity == "error"

    def test_severity_warning(self, sample_df):
        """Severidad warning."""
        rule = RequiredColumnsRule(columns=["nonexistent"], severity="warning")
        result = rule.validate(sample_df)
        
        assert result.severity == "warning"
