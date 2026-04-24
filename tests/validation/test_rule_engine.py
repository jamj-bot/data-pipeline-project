import pytest
import pandas as pd
from data_pipeline.validation.engine.engine import RuleEngine


class TestRuleEngine:
    """Tests para RuleEngine."""

    def test_engine_creation(self):
        """Crear motor de validación."""
        rules_config = [
            {
                "type": "required_columns",
                "columns": ["id", "name"]
            }
        ]
        
        engine = RuleEngine(rules_config)
        
        assert engine is not None
        assert len(engine._rules) == 1

    def test_engine_with_multiple_rules(self):
        """Motor con múltiples reglas."""
        rules_config = [
            {"type": "required_columns", "columns": ["id"]},
            {"type": "column_types", "schema": {"id": "int"}},
        ]
        
        engine = RuleEngine(rules_config)
        
        assert len(engine._rules) == 2

    def test_engine_run_valid_data(self, sample_df):
        """Ejecutar validación en datos válidos."""
        rules_config = [
            {"type": "required_columns", "columns": ["id", "name", "age"]}
        ]
        
        engine = RuleEngine(rules_config)
        report = engine.run(sample_df)
        
        assert report.has_errors() is False
        assert len(report.results) == 1

    def test_engine_run_invalid_data(self, sample_df):
        """Ejecutar validación en datos inválidos."""
        rules_config = [
            {"type": "required_columns", "columns": ["id", "name", "nonexistent"]}
        ]
        
        engine = RuleEngine(rules_config)
        report = engine.run(sample_df)
        
        assert report.has_errors() is True
        assert len(report.errors) == 1

    def test_engine_run_multiple_rules(self, sample_df):
        """Ejecutar múltiples reglas."""
        rules_config = [
            {"type": "required_columns", "columns": ["id", "name"]},
            {"type": "column_types", "schema": {"id": "int", "name": "object"}},
        ]
        
        engine = RuleEngine(rules_config)
        report = engine.run(sample_df)
        
        assert len(report.results) == 2

    def test_engine_with_severity_error(self, sample_df):
        """Regla con severidad error."""
        rules_config = [
            {
                "type": "required_columns",
                "columns": ["nonexistent"],
                "severity": "error"
            }
        ]
        
        engine = RuleEngine(rules_config)
        report = engine.run(sample_df)
        
        assert len(report.errors) == 1
        assert report.errors[0].severity == "error"

    def test_engine_with_severity_warning(self, sample_df):
        """Regla con severidad warning."""
        rules_config = [
            {
                "type": "required_columns",
                "columns": ["nonexistent"],
                "severity": "warning"
            }
        ]
        
        engine = RuleEngine(rules_config)
        report = engine.run(sample_df)
        
        assert len(report.warnings) == 1
        assert report.warnings[0].severity == "warning"
