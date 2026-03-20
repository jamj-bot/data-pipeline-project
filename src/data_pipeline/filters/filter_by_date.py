import pandas as pd

from data_pipeline.core.filter import DataFilter

class FilterByDateRange(DataFilter):
    """ Filtro que selecciona registros dentro de un rango de fechas."""
    def __init__(self, start_date: str, end_date: str) -> None:
        self._start_date = pd.to_datetime(start_date)
        self._end_date = pd.to_datetime(end_date)

        if self._start_date > self._end_date:
            raise ValueError("start_date no puede ser posterior que end_date")

    def process(self, data: pd.DataFrame | None) -> pd.DataFrame:
        if data is None:
            raise ValueError("FilterByDateRange requiere un DataFrame como Entrada")

        if "FL_DATE" not in data.columns:
            raise ValueError("El DataFrame debe tener una columna llamada 'Date' ")

        df = data.copy() # Copia defensiva
        # Convierte la columna "date" a datetime64[ns]
        df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])
        # Crea máscara booleana que selecciona las filas que cumplen con ambas condiciones
        mask = (df["FL_DATE"] >= self._start_date) & (df["FL_DATE"] <= self._end_date)

        # Retorna nuevo dataframe que contiene solo las filas que cumple true en la máscara booleana
        return df.loc[mask]
