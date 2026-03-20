import pandas as pd

from data_pipeline.core.filter import DataFilter

class CleanDataFilter(DataFilter):
    """
    Filtro encargado de realizar una limpieza básica de los datos.
    """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        if data is None:
            raise ValueError("CleanDataFilter requiere un DataFrame de Entrada.")

        return data.dropna(how="all")
