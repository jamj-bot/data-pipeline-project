import pandas as pd
import logging
from data_pipeline.core.filter import DataFilter
from data_pipeline.validation.engine.engine import RuleEngine


class SchemaValidationFilter(DataFilter):

    def __init__(self, rules: list[dict]):
        self._engine = RuleEngine(rules)
        self._logger = logging.getLogger("DataPipeline")

    def process(self, data: pd.DataFrame) -> pd.DataFrame:

        report = self._engine.run(data)

        summary = report.summary()
        self._logger.info(f"Validation summary: {summary}")

        # Manejo de warnings
        for warning in report.warnings:
            self._logger.warning(
                f"[{warning.rule_name}] {' | '.join(warning.errors)}"
            )

        # Manejo de errores
        if report.has_errors():

            error_messages = [
                f"[{e.rule_name}] {' | '.join(e.errors)}"
                for e in report.errors
            ]

            self._logger.error(
                "Validation failed: " + " | ".join(error_messages)
            )

            raise ValueError(" | ".join(error_messages))

        return data
