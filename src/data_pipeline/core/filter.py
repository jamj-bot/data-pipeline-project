from abc import ABC, abstractmethod
import pandas as pd


class DataFilter(ABC):
    """
    Contrato base para filtros de transformación.

    - SIEMPRE recibe un DataFrame
    - SIEMPRE devuelve un DataFrame
    """

    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
