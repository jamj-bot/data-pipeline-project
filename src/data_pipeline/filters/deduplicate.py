import pandas as pd

from data_pipeline.core.filter import DataFilter

class DeduplicateFilter(DataFilter):
    """
    Filtro encargado de eliminar filas duplicadas.
    """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        if data is None:
            raise ValueError("DeduplicateFilter requiere un DataFrame de Entrada.")

        return data.drop_duplicates()
