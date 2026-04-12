import pandas as pd
import logging
import json
from pathlib import Path
from data_pipeline.core.filter import DataFilter
from data_pipeline.validation.engine.engine import RuleEngine


class SchemaValidationFilter(DataFilter):

    def __init__(
        self,
        rules: list[dict],
        fail_on: dict | None = None,
        report_path: str | None = None,
        row_actions: dict | None = None
    ):
        self._engine = RuleEngine(rules)
        self._logger = logging.getLogger("DataPipeline")

        self._report_path = report_path

        # NEW: fail config (backward compatible)
        self._fail_config = {
            "error": self._parse_fail_config(
                fail_on.get("error", True) if fail_on else True
            ),
            "warning": self._parse_fail_config(
                fail_on.get("warning", False) if fail_on else False
            )
        }

        # Row-level actions
        self._on_error_action = "fail"
        self._on_warning_action = "keep"

        if row_actions:
            self._on_error_action = row_actions.get("error", "fail")
            self._on_warning_action = row_actions.get("warning", "keep")

    def _parse_fail_config(self, value):
        if isinstance(value, bool):
            return {
                "enabled": value,
                "strategy": "pre"
            }

        return {
            "enabled": True,
            "strategy": value.get("strategy", "pre"),
            "threshold": value.get("threshold")
        }

    def _drop_rows(self, data: pd.DataFrame, rows: set[int]) -> pd.DataFrame:
        if not rows:
            return data
        return data.drop(index=list(rows))

    def _should_fail_pre(self, report, severity):
        config = self._fail_config[severity]

        if not (config["enabled"] and config["strategy"] == "pre"):
            return False

        return report.has_errors() if severity == "error" else report.has_warnings()

    def _should_fail_post(self, data, severity):
        config = self._fail_config[severity]

        if not (config["enabled"] and config["strategy"] == "post"):
            return False

        new_report = self._engine.run(data)

        return (
            new_report.has_errors()
            if severity == "error"
            else new_report.has_warnings()
        )

    def _should_fail_threshold(self, original_count, invalid_rows, severity):
        config = self._fail_config[severity]

        if config["strategy"] != "threshold":
            return False

        threshold = config.get("threshold", 0)
        ratio = len(invalid_rows) / max(original_count, 1)

        self._logger.info(
            f"[{severity}] invalid ratio: {ratio:.4f} (threshold={threshold})"
        )

        return ratio > threshold

    def process(self, data: pd.DataFrame) -> pd.DataFrame:

        original_row_count = len(data)

        report = self._engine.run(data)

        # =========================
        # LOGGING (UNCHANGED)
        # =========================

        summary = report.summary()
        self._logger.info(f"Validation summary: {summary}")

        for warning in report.warnings:
            self._logger.warning(
                f"[{warning.rule_name}] {' | '.join(warning.errors)}"
            )

        if self._report_path:
            path = Path(self._report_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w") as f:
                json.dump(report.to_dict(), f, indent=2)

            self._logger.info(f"Validation report saved to {self._report_path}")

        # =========================
        # PRE FAIL (NEW)
        # =========================

        if self._should_fail_pre(report, "warning"):
            raise ValueError("Validation failed (pre warning)")

        if self._should_fail_pre(report, "error"):
            raise ValueError("Validation failed (pre error)")

        # =========================
        # ROW-LEVEL HANDLING
        # =========================

        error_rows = report.invalid_rows("error")
        warning_rows = report.invalid_rows("warning")

        if error_rows:
            if self._on_error_action == "drop":
                data = self._drop_rows(data, error_rows)
                self._logger.info(
                    f"Dropped {len(error_rows)} rows due to validation errors"
                )

            elif self._on_error_action == "separate":
                invalid_df = data.loc[list(error_rows)]
                data = self._drop_rows(data, error_rows)

                self._logger.info(
                    f"Separated {len(error_rows)} invalid rows (errors)"
                )

        if warning_rows:
            if self._on_warning_action == "drop":
                data = self._drop_rows(data, warning_rows)
                self._logger.info(
                    f"Dropped {len(warning_rows)} rows due to warnings"
                )

            elif self._on_warning_action == "separate":
                invalid_df = data.loc[list(warning_rows)]
                data = self._drop_rows(data, warning_rows)

                self._logger.info(
                    f"Separated {len(warning_rows)} invalid rows (warnings)"
                )

        # =========================
        # POST FAIL (NEW)
        # =========================

        if self._should_fail_post(data, "warning"):
            raise ValueError("Validation failed (post warning)")

        if self._should_fail_post(data, "error"):
            raise ValueError("Validation failed (post error)")

        # =========================
        # THRESHOLD FAIL (NEW)
        # =========================

        if self._should_fail_threshold(original_row_count, error_rows, "error"):
            raise ValueError("Validation failed (threshold error)")

        if self._should_fail_threshold(original_row_count, warning_rows, "warning"):
            raise ValueError("Validation failed (threshold warning)")

        return data
