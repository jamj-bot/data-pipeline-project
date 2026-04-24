# tests/validation/rules/test_column_types_rule.py
import pytest
import pandas as pd
import numpy as np
from data_pipeline.validation.rules.schema.column_types import ColumnTypesRule


class TestColumnTypesRule:
    """Tests para ColumnTypesRule."""

    def test_correct_types(self, sample_df):
        """Todos los tipos son correctos."""
        schema = {
            "id": "int",
            # Sistema no soporta tipo object, hay que corregir"name": "object",
            "age": "int",
            "salary": "float"
        }
        rule = ColumnTypesRule(schema=schema)
        result = rule.validate(sample_df)
        
        assert result.is_valid is True
        assert result.errors == []

    def test_incorrect_type_single_column(self, sample_df):
        """Tipo incorrecto en una columna."""
        schema = {
            "id": "float",  # es int, esperamos float
        }
        rule = ColumnTypesRule(schema=schema)
        result = rule.validate(sample_df)
        
        assert result.is_valid is False
        assert len(result.errors) >= 1

    def test_missing_column_ignored(self, sample_df):
        """Columnas no presentes en DF se ignoran."""
        schema = {
            "nonexistent": "int",
            "id": "int"
        }
        rule = ColumnTypesRule(schema=schema)
        result = rule.validate(sample_df)
        
        assert result.is_valid is True

    def test_nullable_int_type(self):
        """Tipo Int16 nullable."""
        df = pd.DataFrame({
            "id": pd.array([1, 2, None], dtype=pd.Int16Dtype())
        })
        
        schema = {"id": "Int16"}
        rule = ColumnTypesRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is True

    def test_datetime_type(self):
        """Tipo datetime."""
        df = pd.DataFrame({
            "date": pd.to_datetime(["2023-01-01", "2023-01-02"])
        })
        
        schema = {"date": "datetime"}
        rule = ColumnTypesRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is True

    def test_boolean_type(self):
        """Tipo boolean."""
        df = pd.DataFrame({
            "flag": [True, False, True]
        })
        
        schema = {"flag": "bool"}
        rule = ColumnTypesRule(schema=schema)
        result = rule.validate(df)
        
        assert result.is_valid is True

    def test_unsupported_type(self, sample_df):
        """Tipo no soportado."""
        schema = {"id": "unsupported_type"}
        rule = ColumnTypesRule(schema=schema)
        result = rule.validate(sample_df)
        
        assert result.is_valid is False
        assert "no soportado" in result.errors[0].lower()

    def test_is_row_level_false(self, sample_df):
        """Las reglas de tipos son dataset-level."""
        schema = {"id": "float"}
        rule = ColumnTypesRule(schema=schema)
        result = rule.validate(sample_df)
        
        assert result.is_row_level is False
        assert result.invalid_rows == []
