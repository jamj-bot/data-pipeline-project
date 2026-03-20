import pandas as pd

from data_pipeline.core.filter import DataFilter

class SaveCSVFilter(DataFilter):
    """
        Filtro encargado de guardar el DataFrame resultante en un archivo CSV.
    """

    def __init__(self, output_path: str, index: bool = False) -> None:
        self._output_path = output_path
        self._index = index

    def process(self, data: pd.DataFrame | None) ->pd.DataFrame:
        if data is None:
            raise ValueError("SaveCSVFilter requiere un DataFrame como Entrada")

        data.to_csv(self._output_path, index=self._index)
        return data

