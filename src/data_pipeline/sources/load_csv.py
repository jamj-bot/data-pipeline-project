import pandas as pd
from pathlib import Path

from data_pipeline.core.data_source import DataSource


class LoadCSVFilter(DataSource):
    """
    Fuente de datos desde CSV.
    """

    def __init__(self, file_path: str):
        self._file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        if not self._file_path.exists():
            raise FileNotFoundError(f"Archivo CSV no encontrado: {self._file_path}")

        df = pd.read_csv(self._file_path)

        if df.empty:
            raise ValueError("El DataFrame cargado está vacío")

        return df
