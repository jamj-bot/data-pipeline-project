import pandas as pd
from pathlib import Path

from data_pipeline.core.filter import DataFilter

class LoadCSVFilter(DataFilter):
    """
    Filtro encargado de cargar datos desde un archivo CSV.
    """
    def __init__(self, file_path: str):
        self._file_path = Path(file_path)

    def process(self, data=None) -> pd.DataFrame:
        if not self._file_path.exists():
            raise FileNotFoundError(f"Archivo CSV no encontrado: {self._file_path}")

        df = pd.read_csv(self._file_path)

        if df.empty:
            raise ValueError("El DataFrame cargado está vacio")

        return df



    # def __init__(self, file_path: str) -> None:
    #     self._file_path = file_path

    # def process(self, data: pd.DataFrame | None) -> pd.DataFrame:
    #     """
    #     Carga el CSV desde disco y devuelve un DataFrame.

    #     :param data: No se utiliza (primer filtro de la pipeline)
    #     :return: DataFrame con los datos cargados
    #     """
    #     return pd.read_csv(self._file_path)
