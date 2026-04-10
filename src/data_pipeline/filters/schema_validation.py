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

        # Default behavior (backward compatibility)
        self._fail_on_error = True
        self._fail_on_warning = False

        if fail_on:
            self._fail_on_error = fail_on.get("error", True)
            self._fail_on_warning = fail_on.get("warning", False)

        # Row-level actions
        self._on_error_action = "fail"
        self._on_warning_action = "keep"

        if row_actions:
            self._on_error_action = row_actions.get("error", "fail")
            self._on_warning_action = row_actions.get("warning", "keep")

    def _drop_rows(self, data: pd.DataFrame, rows: set[int]) -> pd.DataFrame:
        if not rows:
            return data
        return data.drop(index=list(rows))

    def process(self, data: pd.DataFrame) -> pd.DataFrame:

        report = self._engine.run(data)

        # Summary
        summary = report.summary()
        self._logger.info(f"Validation summary: {summary}")

        # Warnings
        for warning in report.warnings:
            self._logger.warning(
                f"[{warning.rule_name}] {' | '.join(warning.errors)}"
            )

        # Persist report
        if self._report_path:
            path = Path(self._report_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w") as f:
                json.dump(report.to_dict(), f, indent=2)

            self._logger.info(f"Validation report saved to {self._report_path}")

        # =========================
        # ROW-LEVEL HANDLING 
        # =========================

        error_rows = report.invalid_rows("error")
        warning_rows = report.invalid_rows("warning")

        # Handle error rows
        if error_rows:
            if self._on_error_action == "drop":
                data = self._drop_rows(data, error_rows)
                self._logger.info(
                    f"Dropped {len(error_rows)} rows due to validation errors"
                )

            elif self._on_error_action == "separate":
                invalid_df = data.loc[list(error_rows)]
                valid_df = self._drop_rows(data, error_rows)

                self._logger.info(
                    f"Separated {len(error_rows)} invalid rows (errors)"
                )

                # FUTURE: persist invalid_df
                data = valid_df

            elif self._on_error_action == "keep":
                pass

            elif self._on_error_action == "fail":
                pass  # handled below

        # Handle warning rows
        if warning_rows:
            if self._on_warning_action == "drop":
                data = self._drop_rows(data, warning_rows)
                self._logger.info(
                    f"Dropped {len(warning_rows)} rows due to warnings"
                )

            elif self._on_warning_action == "separate":
                invalid_df = data.loc[list(warning_rows)]
                valid_df = self._drop_rows(data, warning_rows)

                self._logger.info(
                    f"Separated {len(warning_rows)} invalid rows (warnings)"
                )

                data = valid_df

            elif self._on_warning_action == "keep":
                pass

        # =========================
        # FAIL POLICIES
        # =========================

        if self._fail_on_warning and report.has_warnings():
            warning_messages = [
                f"[{w.rule_name}] {' | '.join(w.errors)}"
                for w in report.warnings
            ]

            self._logger.error(
                "Validation failed (warnings): " + " | ".join(warning_messages)
            )

            raise ValueError(" | ".join(warning_messages))

        if self._fail_on_error and report.has_errors():

            error_messages = [
                f"[{e.rule_name}] {' | '.join(e.errors)}"
                for e in report.errors
            ]

            self._logger.error(
                "Validation failed (errors): " + " | ".join(error_messages)
            )

            raise ValueError(" | ".join(error_messages))

        return data
