import pandas as pd
from pathlib import Path

from data_pipeline.core.filter import DataFilter

class ChunkedCSVFilter(DataFilter):
    """
    Filtro encargado de cargar datos chunkeados desde un archivo CSV.
    """
    def __init__(self, file_path: str):
        self._file_path = Path(file_path)

    def process(self, data=None) -> pd.DataFrame:
        if not self._file_path.exists():
            raise FileNotFoundError(f"Archivo CSV no encontrado: {self._file_path}")


        for chunk in pd.read_csv(self._file_path, chunksize=100):
            df = chunk
            break

        if df.empty:
            raise ValueError("El DataFrame cargado está vacio")

        return df

