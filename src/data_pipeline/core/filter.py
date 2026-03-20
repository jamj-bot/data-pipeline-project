from abc import ABC, abstractmethod
import pandas as pd


class DataFilter(object):
    """
    Contrato base para todos los filtros de la pipeline.

    Un filtro:
    - Recibe un DataFrame
    - Aplica una transformación
    - Devuelve un nuevo DataFrame
    """

    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Procesa los datos de entrada y devuelve los datos transformados.

        :param data: DataFrame de entrada
        :return: DataFrame transformado
        """
        pass


