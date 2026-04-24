# tests/validation/test_validation_report.py
import pytest
from data_pipeline.validation.result import ValidationResult
from data_pipeline.validation.validation_report import ValidationReport


class TestValidationReport:
    """Tests para ValidationReport."""

    def test_add_result(self):
        """Agregar un resultado al reporte."""
        report = ValidationReport()
        result = ValidationResult(
            rule_name="TestRule",
            is_valid=True,
            errors=[]
        )
        
        report.add(result)
        
        assert len(report.results) == 1
        assert report.results[0] == result

    def test_add_multiple_results(self):
        """Agregar múltiples resultados."""
        report = ValidationReport()
        results = [
            ValidationResult("Rule1", True, []),
            ValidationResult("Rule2", False, ["Error"]),
            ValidationResult("Rule3", True, []),
        ]
        
        for result in results:
            report.add(result)
        
        assert len(report.results) == 3

    def test_errors_property(self):
        """Filtrar resultados con errores."""
        report = ValidationReport()
        report.add(ValidationResult("Rule1", True, [], severity="error"))
        report.add(ValidationResult("Rule2", False, ["Error"], severity="error"))
        report.add(ValidationResult("Rule3", False, ["Warning"], severity="warning"))
        
        errors = report.errors
        
        assert len(errors) == 1
        assert errors[0].rule_name == "Rule2"

    def test_warnings_property(self):
        """Filtrar resultados con warnings."""
        report = ValidationReport()
        report.add(ValidationResult("Rule1", False, ["Error"], severity="error"))
        report.add(ValidationResult("Rule2", False, ["Warning"], severity="warning"))
        report.add(ValidationResult("Rule3", False, ["Warning2"], severity="warning"))
        
        warnings = report.warnings
        
        assert len(warnings) == 2

    def test_has_errors(self):
        """Detectar presencia de errores."""
        report_without_errors = ValidationReport()
        report_without_errors.add(ValidationResult("Rule1", True, []))
        assert report_without_errors.has_errors() is False
        
        report_with_errors = ValidationReport()
        report_with_errors.add(ValidationResult("Rule1", False, ["Error"], severity="error"))
        assert report_with_errors.has_errors() is True

    def test_has_warnings(self):
        """Detectar presencia de warnings."""
        report_without_warnings = ValidationReport()
        report_without_warnings.add(ValidationResult("Rule1", True, []))
        assert report_without_warnings.has_warnings() is False
        
        report_with_warnings = ValidationReport()
        report_with_warnings.add(ValidationResult("Rule1", False, ["Warning"], severity="warning"))
        assert report_with_warnings.has_warnings() is True

    def test_invalid_rows_only_row_level(self):
        """invalid_rows solo incluye reglas row-level."""
        report = ValidationReport()
        report.add(ValidationResult(
            "DatasetRule",
            False,
            ["Error"],
            severity="error",
            is_row_level=False,
            invalid_rows=[]
        ))
        report.add(ValidationResult(
            "RowRule",
            False,
            ["Error"],
            severity="error",
            is_row_level=True,
            invalid_rows=[0, 1, 2]
        ))
        
        invalid_rows = report.invalid_rows("error")
        
        assert invalid_rows == {0, 1, 2}

    def test_invalid_rows_by_severity(self):
        """invalid_rows filtra por severidad."""
        report = ValidationReport()
        report.add(ValidationResult(
            "ErrorRule",
            False,
            ["Error"],
            severity="error",
            is_row_level=True,
            invalid_rows=[0, 1]
        ))
        report.add(ValidationResult(
            "WarningRule",
            False,
            ["Warning"],
            severity="warning",
            is_row_level=True,
            invalid_rows=[2, 3]
        ))
        
        error_rows = report.invalid_rows("error")
        warning_rows = report.invalid_rows("warning")
        
        assert error_rows == {0, 1}
        assert warning_rows == {2, 3}

    def test_summary(self):
        """Generar resumen del reporte."""
        report = ValidationReport()
        report.add(ValidationResult("Rule1", True, []))
        report.add(ValidationResult("Rule2", False, ["Error"], severity="error"))
        report.add(ValidationResult("Rule3", False, ["Warning"], severity="warning"))
        
        summary = report.summary()
        
        assert summary["total_rules"] == 3
        assert summary["errors"] == 1
        assert summary["warnings"] == 1

    def test_to_dict(self):
        """Convertir reporte a diccionario."""
        report = ValidationReport()
        report.add(ValidationResult(
            "Rule1",
            False,
            ["Error 1"],
            severity="error",
            is_row_level=False
        ))
        report.add(ValidationResult(
            "Rule2",
            False,
            ["Invalid value"],
            severity="error",
            is_row_level=True,
            invalid_rows=[0, 1]
        ))
        
        report_dict = report.to_dict()
        
        assert "summary" in report_dict
        assert "errors" in report_dict
        assert "warnings" in report_dict
        assert "row_level" in report_dict
        assert len(report_dict["errors"]) == 2





