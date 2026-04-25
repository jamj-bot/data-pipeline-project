import pytest
import pandas as pd
from data_pipeline.filters.data_quality_metrics import DataQualityMetricsFilter


class TestDataQualityMetricsFilter:
    """Tests para DataQualityMetricsFilter."""

    def test_process_returns_same_dataframe(self, sample_df, caplog):
        """El filtro retorna el mismo DataFrame sin modificarlo."""
        filter_ = DataQualityMetricsFilter()
        result = filter_.process(sample_df)
        
        assert result.equals(sample_df)

    def test_logs_general_info(self, sample_df, caplog):
        """Se registra información general del DataFrame."""
        filter_ = DataQualityMetricsFilter()
        filter_.process(sample_df)
        
        # Verifica que se haya logeado algo
        assert len(caplog.records) > 0

    def test_none_input_raises(self):
        """Entrada None debe lanzar excepción."""
        filter_ = DataQualityMetricsFilter()
        
        with pytest.raises(ValueError):
            filter_.process(None)

    def test_reports_total_rows(self, sample_df, caplog):
        """Se reporta el número total de filas."""
        filter_ = DataQualityMetricsFilter()
        filter_.process(sample_df)
        
        log_text = caplog.text
        assert "Filas_Totales" in log_text or "5" in log_text

    def test_reports_duplicates(self, sample_df_with_duplicates, caplog):
        """Se reportan filas duplicadas."""
        filter_ = DataQualityMetricsFilter()
        filter_.process(sample_df_with_duplicates)
        
        log_text = caplog.text
        assert "Filas_Duplicadas" in log_text

    def test_reports_nulls(self, sample_df_with_nulls, caplog):
        """Se reportan valores nulos."""
        filter_ = DataQualityMetricsFilter()
        filter_.process(sample_df_with_nulls)
        
        log_text = caplog.text
        assert "Valores_nulos" in log_text or "nulos" in log_text.lower()

    def test_no_nulls(self, sample_df, caplog):
        """Reporte cuando no hay nulos."""
        filter_ = DataQualityMetricsFilter()
        filter_.process(sample_df)
        
        log_text = caplog.text
        # Debe reportar 0 nulos en algún punto
        assert "0" in log_text or "nulos" in log_text.lower()

    def test_all_nulls_column(self):
        """Columna completamente nula."""
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "all_null": [None, None, None]
        })
        
        filter_ = DataQualityMetricsFilter()
        result = filter_.process(df)
        
        assert result.equals(df)

    def test_empty_dataframe(self):
        """DataFrame vacío."""
        df = pd.DataFrame()
        filter_ = DataQualityMetricsFilter()
        result = filter_.process(df)
        
        assert result.empty

    def test_large_dataframe_performance(self):
        """Performance con DataFrame grande."""
        df = pd.DataFrame({
            "col1": range(10000),
            "col2": range(10000, 20000)
        })
        
        filter_ = DataQualityMetricsFilter()
        result = filter_.process(df)
        
        assert len(result) == 10000
