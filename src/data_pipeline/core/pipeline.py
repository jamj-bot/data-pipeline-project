import pandas as pd
import time
from typing import List, Optional
from data_pipeline.core.filter import DataFilter
from data_pipeline.core.logger import get_logger

class DataPipeline():
    """ Orquestador de filtros bajo el patrón Pipes & Filters. """
    def __init__(self, filters: list[DataFilter]) -> None:
        self._filters = filters
        # Crea un logger y lo guarda como objeto privado de la clase con el nombre de la clase
        self._logger = get_logger(self.__class__.__name__)

    def run(self) -> pd.DataFrame:
        """
        Ejecuta la pipeline completa en orden.
        :return: DataFrame resultante
        """
        data: Optional[pd.DataFrame] = None
        self._logger.info("Pipeline iniciada") # Crea mensaje en el logger de la clase

        for data_filter in self._filters:
            filter_name = data_filter.__class__.__name__
            start_time = time.perf_counter()

            input_rows = len(data) if data is not None else 0
            data = data_filter.process(data)
            output_rows = len(data) if data is not None else 0
            duration = time.perf_counter() - start_time

            self._logger.info(
                f"{filter_name}: In {input_rows:,} → Out {output_rows:,} ({duration:.4f}s)"
            )

        if data is None:
            raise RuntimeError("La Pipeline se ejecutó sin producir datos.")

        self._logger.info("Pipeline finalizada correctamente")  # Crea mensaje en el logger de la clase

        return data


