import pandas as pd
import logging
from data_pipeline.core.filter import DataFilter
from data_pipeline.validation.engine.engine import RuleEngine


class SchemaValidationFilter:

    def __init__(self, rules: list[dict]):
        self._engine = RuleEngine(rules)

    def process(self, data):

        report = self._engine.run(data)

        logger = logging.getLogger("DataPipeline")

        # Manejo de warnings
        for warning in report.warnings:
            logger.warning(
                f"[{warning.rule_name}] {' | '.join(warning.errors)}"
            )
            
        # Manejo de errores
        if report.has_errors():
            error_messages = [
                f"[{e.rule_name}] {e.errors}"
                for e in report.errors
            ]
            raise ValueError(" | ".join(error_messages))

        return data
