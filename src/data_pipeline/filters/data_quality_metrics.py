import io
import pandas as pd

from data_pipeline.core.filter import DataFilter
from data_pipeline.core.logger import get_logger


class DataQualityMetricsFilter(DataFilter):
    """ Calcula métricas básicas de calidad de datos.
        No modifica el DataFrame
    """
    def __init__(self) -> None:
        self._logger = get_logger(self.__class__.__name__)

    def process(self, data: pd.DataFrame | None) -> pd.DataFrame:
        if data is None:
            raise ValueError("DataQualityMetricsFilter requiere un DataFrame como entrada")

        self._logger.info(f">>> Inicio: General Info")

        buffer = io.StringIO()
        data.info(buf=buffer)
        self._logger.info(f"\n{buffer.getvalue()}")

        self._logger.info(f">>> Fin: General Info")

        total_rows = len(data)
        duplicate_rows = data.duplicated().sum()
        duplicated_percentage = (duplicate_rows / total_rows) * 100 if total_rows > 0 else 0

        null_counts = data.isna().sum()

        total_isnull_count = data.isnull().sum().sum()
        null_cells_percentage = (total_isnull_count / data.size) * 100 if data.size > 0 else 0

        max_col_length = max((len(str(col)) for col in null_counts.keys()), default=0)

        self._logger.info(f">>> Inicio: Metrics")

        self._logger.info(f"\tFilas_Totales: {total_rows:,}")
        self._logger.info(f"\tFilas_Duplicadas: {duplicate_rows} ({duplicated_percentage:.4f}%)")

        for column, nulls in null_counts.items():
            percentage = (nulls / total_rows) * 100 if total_rows > 0 else 0
            self._logger.info(
                f"\tColumna: {column:<{max_col_length}} | Valores_nulos: {nulls} ({percentage:.4f}%)"
            )

        self._logger.info(f"\tNulos_Totales: {total_isnull_count:,} ({null_cells_percentage:.4f}%)")

        self._logger.info(f"<<< Fin: Metrics")

        return data
