import pytest
import pandas as pd

from data_pipeline.filters.data_type_converter import DataTypeConverterFilter


class TestDataTypeConverterFilter:
    
    def test_data_type_converter_does_not_mutate_input(self):
        df = pd.DataFrame({
            "value": ["1", "2"]
        })

        original = df.copy(deep=True)

        filter_ = DataTypeConverterFilter({
            "value": "Int16"
        })

        filter_.process(df)

        assert df.equals(original)

