import pandas as pd
import pytest

from data_pipeline.filters.filter_by_date import FilterByDateRange

def test_filter_by_date_range_filters_correctly():
    df = pd.DataFrame({      
        "FL_DATE": [
            "2024-01-01", "2024-01-10",
            "2024-01-20", "2024-01-30",
        ],
        "revenue": [100, 200, 300, 400],
    })

    filter_ = FilterByDateRange("2024-01-05", "2024-01-20")
    result = filter_.process(df)

    assert len(result) == 2
    assert result["revenue"].sum() == 500

def test_filter_by_date_requires_date_column():
    df = pd.DataFrame({"revenue": [100, 200]})
    filter_ = FilterByDateRange("2024-01-01", "2024-01-10")

    with pytest.raises(ValueError):
        filter_.process(df)

def test_filter_by_date_invalid_range():
    with pytest.raises(ValueError):
        FilterByDateRange("2024-02-01", "2024-01-01")
