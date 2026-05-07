from abc import ABC, abstractmethod
import pandas as pd


class DataSink(ABC):
    """
    Represents a data output target.

    Unlike DataFilter:
    - Receives a DataFrame
    - Produces side effects (I/O)
    - May return DataFrame for pipeline continuity
    """

    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
