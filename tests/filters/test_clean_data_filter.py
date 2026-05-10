import pandas as pd
import pytest

from data_pipeline.filters.clean_data import CleanDataFilter


class TestCleanDataFilter:
    
    def test_clean_data_does_not_mutate_input(self):
        df = pd.DataFrame({
            "a": [1, None],
            "b": [2, None]
        })

        original = df.copy(deep=True)

        filter_ = CleanDataFilter()

        filter_.process(df)

        assert df.equals(original)

    def test_clean_data_removes_fully_null_rows(self):
        # Arrange: DataFrame de entrada
        df = pd.DataFrame({
            "A": [1, None, 3],
            "B": [4, None, 6],
        })


        # act: ejecutar el filtro
        result = CleanDataFilter().process(df)

        # assert la fila completamente nula fue eliminada
        assert len(result) == 2

    def test_clean_data_raises_when_input_is_none(self):
        filter_ = CleanDataFilter()

        with pytest.raises(ValueError):
            filter_.process(None)



