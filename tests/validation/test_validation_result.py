import pytest
from data_pipeline.validation.result import ValidationResult


class TestValidationResult:
    """Tests para el modelo ValidationResult."""

    def test_creation_valid_result(self):
        """Crear un resultado válido."""
        result = ValidationResult(
            rule_name="TestRule",
            is_valid=True,
            errors=[],
            severity="error"
        )
        
        assert result.rule_name == "TestRule"
        assert result.is_valid is True
        assert result.errors == []
        assert result.severity == "error"
        assert result.is_row_level is False
        assert result.invalid_rows == []

    def test_creation_invalid_result(self):
        """Crear un resultado inválido."""
        result = ValidationResult(
            rule_name="TestRule",
            is_valid=False,
            errors=["Error 1", "Error 2"],
            severity="error"
        )
        
        assert result.is_valid is False
        assert len(result.errors) == 2

    def test_dataset_level_result(self):
        """Resultado de nivel dataset (estructural)."""
        result = ValidationResult(
            rule_name="RequiredColumns",
            is_valid=False,
            errors=["Missing columns: {'col1'}"],
            severity="error",
            is_row_level=False,
            invalid_rows=[]
        )
        
        assert result.is_row_level is False
        assert result.invalid_rows == []

    def test_row_level_result(self):
        """Resultado de nivel fila (semántico)."""
        result = ValidationResult(
            rule_name="ValueRange",
            is_valid=False,
            errors=["Values out of range in column 'age'"],
            severity="error",
            is_row_level=True,
            invalid_rows=[0, 2, 4]
        )
        
        assert result.is_row_level is True
        assert result.invalid_rows == [0, 2, 4]

    def test_warning_severity(self):
        """Resultado con severidad warning."""
        result = ValidationResult(
            rule_name="TestRule",
            is_valid=False,
            errors=["Warning message"],
            severity="warning"
        )
        
        assert result.severity == "warning"

    def test_error_severity(self):
        """Resultado con severidad error."""
        result = ValidationResult(
            rule_name="TestRule",
            is_valid=False,
            errors=["Error message"],
            severity="error"
        )
        
        assert result.severity == "error"

    def test_invalid_rows_always_list(self):
        """invalid_rows siempre debe ser una lista."""
        result = ValidationResult(
            rule_name="TestRule",
            is_valid=False,
            errors=[],
            is_row_level=False
        )
        
        assert isinstance(result.invalid_rows, list)
        assert result.invalid_rows == []
