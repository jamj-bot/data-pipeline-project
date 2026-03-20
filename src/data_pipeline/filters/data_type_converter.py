import pandas as pd
from data_pipeline.core.filter import DataFilter

UNIT_MAP = {
    "seconds": "s",
    "minutes": "m",
    "hours": "h",
    "days": "d"
}


class DataTypeConverterFilter(DataFilter):
    """ Convierte el tipo de dato de columnas dadas
    """
    def __init__(self, dtype_mapping: dict):
        """
        dtype_mapping puede ser:

        Formato simple:
            {'col': 'Int16'}

        Formato estructurado:
            {'col': {'dtype': 'timedelta', 'unit': 'minutes'}}
        """
        self.dtype_mapping = dtype_mapping

    # -------------------------------------------------
    # Normalizador de configuración (retrocompatibilidad)
    # -------------------------------------------------
    def _normalize_spec(self, spec):

        if isinstance(spec, str):
            return {"dtype": spec}

        if isinstance(spec, dict):
            if "dtype" not in spec:
                raise ValueError("Spec estructurado debe contener 'dtype'")
            return spec

        raise TypeError("dtype_mapping debe contener string o dict")

    # -------------------------------------------------
    # Conversión principal
    # -------------------------------------------------
    def process(self, data: pd.DataFrame) -> pd.DataFrame:

        for col, raw_spec in self.dtype_mapping.items():

            if col not in data.columns:
                raise ValueError(f"Columna '{col}' no existe")

            spec = self._normalize_spec(raw_spec)

            dtype = spec["dtype"]
            unit = spec.get("unit")

            # -------- DATETIME --------
            if dtype.startswith("datetime") or dtype == "datetime":

                data[col] = pd.to_datetime(
                    data[col],
                    errors="coerce",
                    utc=spec.get("utc", False)
                )

            # -------- TIMEDELTA --------
            elif dtype.startswith("timedelta") or dtype == "timedelta":

                if not unit:
                    raise ValueError(
                        f"Columna '{col}' requiere 'unit' para timedelta"
                    )

                if unit not in UNIT_MAP:
                    raise ValueError(f"Unidad '{unit}' no soportada")

                data[col] = pd.to_timedelta(
                    data[col],
                    unit=UNIT_MAP[unit],
                    errors="coerce"
                )

            # -------- NUMERIC --------
            elif "int" in dtype.lower() or "float" in dtype.lower():

                data[col] = pd.to_numeric(
                    data[col],
                    errors="coerce"
                ).astype(dtype)

            # -------- STRING --------
            elif dtype == "string":

                data[col] = data[col].astype("string")

            # -------- BOOLEAN --------
            elif dtype in ["bool", "boolean"]:

                data[col] = data[col].astype("boolean")

            # -------- GENERIC --------
            else:

                data[col] = data[col].astype(dtype)

        return data
