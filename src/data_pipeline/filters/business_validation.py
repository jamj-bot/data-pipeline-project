import pandas as pd
from data_pipeline.core.filter import DataFilter
from data_pipeline.validation.engine.engine import RuleEngine


class BusinessValidationFilter(DataFilter):

    def __init__(self, rules: list[dict]):
        self._engine = RuleEngine(rules)

    def process(self, data: pd.DataFrame) -> pd.DataFrame:

        self._engine.run(data)

        return data
