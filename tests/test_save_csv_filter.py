import pandas as pd
import pytest

from data_pipeline.filters.save_csv import SaveCSVFilter

def test_save_csv_filter_creates_file(tmp_path):
    # Arrange
    df = pd.DataFrame({
        "date" : ["2023-01-01", "2023-01-02"],
        "sales": [100, 200]
    })

    output_file = tmp_path / "output.csv"
    filter_ = SaveCSVFilter(output_path=str(output_file))

    # Act
    result = filter_.process(df)

    # Assert
    assert output_file.exists()
    assert result.equals(df)

    saved_df = pd.read_csv(output_file)
    assert saved_df.shape == df.shape

def test_save_csv_filter_requires_dataframe(tmp_path):
    filter_ = SaveCSVFilter(output_path=str(tmp_path / "out.csv"))

    with pytest.raises(ValueError):
        filter_.process(None)
