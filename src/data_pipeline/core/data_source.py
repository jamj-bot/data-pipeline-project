from abc import ABC, abstractmethod
import pandas as pd


class DataSource(ABC):
    """
    Representa una fuente de datos.

    A diferencia de un DataFilter:
    - NO recibe entrada
    - SIEMPRE produce un DataFrame
    """

    @abstractmethod
    def load(self) -> pd.DataFrame:
        pass
