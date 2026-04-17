import pandas as pd
import time
from typing import List
from data_pipeline.core.filter import DataFilter
from data_pipeline.core.data_source import DataSource
from data_pipeline.core.logger import get_logger


class DataPipeline:
    """ Orquestador de pipeline con fuente explícita. """

    def __init__(
        self,
        source: DataSource,
        filters: List[DataFilter]
    ) -> None:
        self._source = source
        self._filters = filters
        self._logger = get_logger(self.__class__.__name__)

    def run(self) -> pd.DataFrame:
        self._logger.info("Pipeline iniciada")

        start_time = time.perf_counter()
        data = self._source.load()
        duration = time.perf_counter() - start_time

        self._logger.info(
            f"{self._source.__class__.__name__}: Loaded {len(data):,} rows ({duration:.4f}s)"
        )

        for data_filter in self._filters:
            filter_name = data_filter.__class__.__name__
            start_time = time.perf_counter()

            input_rows = len(data)
            data = data_filter.process(data)
            output_rows = len(data)
            duration = time.perf_counter() - start_time

            self._logger.info(
                f"{filter_name}: In {input_rows:,} → Out {output_rows:,} ({duration:.4f}s)"
            )

        self._logger.info("Pipeline finalizada correctamente")

        return data
