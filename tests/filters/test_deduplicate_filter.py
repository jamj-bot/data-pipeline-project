import pytest
import pandas as pd
from data_pipeline.filters.deduplicate import DeduplicateFilter


class TestDeduplicateFilter:
    """Tests para DeduplicateFilter."""

    def test_remove_duplicates(self, sample_df_with_duplicates):
        """Eliminar filas duplicadas."""
        filter_ = DeduplicateFilter()
        result = filter_.process(sample_df_with_duplicates)
        
        assert len(result) == 3
        assert result.duplicated().sum() == 0

    def test_keeps_first_duplicate(self):
        """Se mantiene la primera ocurrencia."""
        df = pd.DataFrame({
            "id": [1, 1, 2],
            "value": [10, 10, 20]
        })
        
        filter_ = DeduplicateFilter()
        result = filter_.process(df)
        
        assert len(result) == 2
        assert result.iloc[0]["value"] == 10

    def test_no_duplicates(self, sample_df):
        """DataFrame sin duplicados."""
        filter_ = DeduplicateFilter()
        result = filter_.process(sample_df)
        
        assert len(result) == len(sample_df)
        assert result.equals(sample_df)

    def test_all_duplicates(self):
        """Todas las filas son duplicadas."""
        df = pd.DataFrame({
            "id": [1, 1, 1],
            "value": [10, 10, 10]
        })
        
        filter_ = DeduplicateFilter()
        result = filter_.process(df)
        
        assert len(result) == 1

    def test_none_input_raises(self):
        """Entrada None debe lanzar excepción."""
        filter_ = DeduplicateFilter()
        
        with pytest.raises(ValueError):
            filter_.process(None)

    def test_empty_dataframe(self):
        """DataFrame vacío."""
        df = pd.DataFrame({"col1": [], "col2": []})
        filter_ = DeduplicateFilter()
        result = filter_.process(df)
        
        assert len(result) == 0

    def test_preserves_columns(self):
        """Se preservan todas las columnas."""
        df = pd.DataFrame({
            "a": [1, 1, 2],
            "b": ["x", "x", "y"],
            "c": [10.0, 10.0, 20.0]
        })
        
        filter_ = DeduplicateFilter()
        result = filter_.process(df)
        
        assert list(result.columns) == ["a", "b", "c"]

    def test_with_null_values(self):
        """Manejo de valores nulos."""
        df = pd.DataFrame({
            "id": [1, None, 1, None],
            "value": [10, 20, 10, 20]
        })
        
        filter_ = DeduplicateFilter()
        result = filter_.process(df)
        
        # Se elimina un [1, 10] y un [None, 20]
        assert len(result) == 2
