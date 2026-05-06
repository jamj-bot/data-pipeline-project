import pandas as pd

from data_pipeline.core.filter import DataFilter

class FilterByDateRange(DataFilter):
    """ Filtro que selecciona registros dentro de un rango de fechas."""
    def __init__(self, start_date: str, end_date: str, field_date: str = "FL_DATE") -> None:
        self._field_date = field_date
        self._start_date = pd.to_datetime(start_date)
        self._end_date = pd.to_datetime(end_date)

        if self._start_date > self._end_date:
            raise ValueError("start_date no puede ser posterior que end_date")

    def process(self, data: pd.DataFrame | None) -> pd.DataFrame:
        if data is None:
            raise ValueError("FilterByDateRange requiere un DataFrame como Entrada")

        if self._field_date not in data.columns:
            raise ValueError(f"El DataFrame debe tener una columna llamada '{self._field_date}'")

        df = data.copy()

        df = df.assign(**{
            self._field_date: pd.to_datetime(df[self._field_date])
        })

        mask = (df[self._field_date] >= self._start_date) & (df[self._field_date] <= self._end_date)

        return df.loc[mask]
