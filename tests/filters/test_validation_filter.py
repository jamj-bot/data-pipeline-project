import pytest
import pandas as pd
import json
from pathlib import Path

from data_pipeline.filters.validation import ValidationFilter


class TestValidationFilter:

    def test_pass_through_when_valid(self, sample_df):
        rules = [
            {"type": "required_columns", "columns": ["id", "name"]}
        ]

        filter_ = ValidationFilter(rules=rules)
        result = filter_.process(sample_df)

        assert result.equals(sample_df)

    def test_fail_on_error_pre(self, sample_df):
        rules = [
            {"type": "required_columns", "columns": ["nonexistent"]}
        ]

        filter_ = ValidationFilter(
            rules=rules,
            fail_on={"error": True}
        )

        with pytest.raises(ValueError):
            filter_.process(sample_df)

    def test_fail_on_warning_pre(self, sample_df):
        rules = [
            {
                "type": "required_columns",
                "columns": ["nonexistent"],
                "severity": "warning"
            }
        ]

        filter_ = ValidationFilter(
            rules=rules,
            fail_on={"warning": True}
        )

        with pytest.raises(ValueError):
            filter_.process(sample_df)

    def test_row_action_drop_error(self):
        df = pd.DataFrame({"age": [10, 50]})

        rules = [
            {
                "type": "value_range",
                "schema": {"age": {"min": 18, "max": 40}}
            }
        ]

        filter_ = ValidationFilter(
            rules=rules,
            row_actions={"error": "drop"},
            fail_on={"error": False}
        )

        result = filter_.process(df)

        assert len(result) == 0

    def test_row_action_keep_default(self):
        df = pd.DataFrame({"age": [10, 50]})

        rules = [
            {
                "type": "value_range",
                "schema": {"age": {"min": 18, "max": 40}}
            }
        ]

        filter_ = ValidationFilter(
            rules=rules,
            fail_on={"error": False}
        )

        result = filter_.process(df)

        assert len(result) == 2

    def test_row_action_separate(self, tmp_path):
        df = pd.DataFrame({"age": [10, 50]})

        rules = [
            {
                "type": "value_range",
                "schema": {"age": {"min": 18, "max": 40}}
            }
        ]

        output_path = tmp_path / "invalid"

        filter_ = ValidationFilter(
            rules=rules,
            row_actions={"error": "separate"},
            invalid_rows_path=str(output_path),
            fail_on={"error": False}
        )

        result = filter_.process(df)

        files = list((tmp_path / "invalid").glob("invalid_rows_error.csv"))
        assert len(files) == 1
        
        assert result.empty
    
    def test_report_file_created(self, sample_df, tmp_path):
        rules = [
            {"type": "required_columns", "columns": ["id"]}
        ]

        report_path = tmp_path / "report.json"

        filter_ = ValidationFilter(
            rules=rules,
            report_path=str(report_path)
        )

        filter_.process(sample_df)

        assert report_path.exists()

        with open(report_path) as f:
            data = json.load(f)

        assert "summary" in data

    def test_fail_on_threshold(self):
        df = pd.DataFrame({"age": [10, 50, 60, 70]})

        rules = [
            {
                "type": "value_range",
                "schema": {"age": {"min": 18, "max": 40}}
            }
        ]

        filter_ = ValidationFilter(
            rules=rules,
            fail_on={"error": {"strategy": "threshold", "threshold": 0.25}}
        )

        with pytest.raises(ValueError):
            filter_.process(df)

    def test_no_fail_when_below_threshold(self):
        df = pd.DataFrame({"age": [10, 20, 30, 40]})

        rules = [
            {
                "type": "value_range",
                "schema": {"age": {"min": 18, "max": 40}}
            }
        ]

        filter_ = ValidationFilter(
            rules=rules,
            fail_on={"error": {"strategy": "threshold", "threshold": 0.5}}
        )

        result = filter_.process(df)

        assert len(result) == 4

    def test_fail_post_strategy(self):
        df = pd.DataFrame({"age": [10, 50]})

        rules = [
            {
                "type": "value_range",
                "schema": {"age": {"min": 18, "max": 40}}
            }
        ]

        filter_ = ValidationFilter(
            rules=rules,
            row_actions={"error": "drop"},
            fail_on={"error": {"strategy": "post"}}
        )

        result = filter_.process(df)
        assert result.empty

    def test_empty_dataframe(self):
        df = pd.DataFrame()

        rules = [
            {"type": "required_columns", "columns": ["id"]}
        ]

        filter_ = ValidationFilter(
            rules=rules,
            fail_on={"error": False}
        )

        result = filter_.process(df)

        assert isinstance(result, pd.DataFrame)
