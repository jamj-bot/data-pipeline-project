import pandas as pd
import logging
from data_pipeline.core.filter import DataFilter
from data_pipeline.validation.engine.engine import RuleEngine


class SchemaValidationFilter(DataFilter):

    def __init__(
        self,
        rules: list[dict],
        fail_on: dict | None = None
    ):
        self._engine = RuleEngine(rules)
        self._logger = logging.getLogger("DataPipeline")

        # Default behavior (backward compatibility)
        self._fail_on_error = True
        self._fail_on_warning = False

        if fail_on:
            self._fail_on_error = fail_on.get("error", True)
            self._fail_on_warning = fail_on.get("warning", False)

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

        # Fail on warnings (optional)
        if self._fail_on_warning and report.has_warnings():
            warning_messages = [
                f"[{w.rule_name}] {' | '.join(w.errors)}"
                for w in report.warnings
            ]

            self._logger.error(
                "Validation failed (warnings): " + " | ".join(warning_messages)
            )

            raise ValueError(" | ".join(warning_messages))

        # Fail on errors (default behavior)
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
