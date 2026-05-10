import pandas as pd
import pytest

from data_pipeline.filters.filter_by_date import FilterByDateRange

class TestFilterByDateRange:

    def test_filter_by_date_does_not_mutate_input(self):
        df = pd.DataFrame({
            "FL_DATE": ["2024-01-01", "2024-01-02"]
        })

        original = df.copy(deep=True)

        filter_ = FilterByDateRange(
            start_date="2024-01-01",
            end_date="2024-01-02"
        )

        filter_.process(df)

        assert df.equals(original)

    def test_filter_by_date_range_filters_correctly(self):
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

    def test_filter_by_date_raises_when_date_column_is_missing(self):
        df = pd.DataFrame({"revenue": [100, 200]})
        filter_ = FilterByDateRange("2024-01-01", "2024-01-10")

        with pytest.raises(ValueError):
            filter_.process(df)

    def test_filter_by_date_raises_when_start_date_is_after_end_date(self):
        with pytest.raises(ValueError):
            FilterByDateRange("2024-02-01", "2024-01-01")
