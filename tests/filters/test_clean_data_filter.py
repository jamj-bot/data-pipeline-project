import pandas as pd
import pytest

from data_pipeline.filters.clean_data import CleanDataFilter

def test_clean_data_removes_fully_null_rows():
    # arrange: dataframe de entrada
    # Arrange: DataFrame de entrada
    df = pd.DataFrame({
        "A": [1, None, 3],
        "B": [4, None, 6],
    })


    # act: ejecutar el filtro
    result = CleanDataFilter().process(df)

    # assert la fila completamente nula fue eliminada
    assert len(result) == 2

def test_clean_data_requires_input_dataframe():
    filter_ = CleanDataFilter()

    with pytest.raises(ValueError):
        filter_.process(None)



