from abc import ABC, abstractmethod
from typing import Type
from data_pipeline.validation.result import ValidationResult
import pandas as pd


RULE_REGISTRY: dict[str, Type["ValidationRule"]] = {}


def register_rule(name: str):
    def decorator(cls):
        RULE_REGISTRY[name] = cls
        return cls
    return decorator


class ValidationRule(ABC):

    def __init__(self, severity: str = "error") -> None:
        self._severity = severity

    @abstractmethod
    def validate(self, data: pd.DataFrame) -> ValidationResult:
        pass

    # =========================
    # ROW-LEVEL HELPERS
    # =========================

    def _init_mask(self, data: pd.DataFrame) -> pd.Series:
        """
        Inicializa una máscara booleana alineada al DataFrame.
        """
        return pd.Series(False, index=data.index)

    def _combine_masks(self, base_mask: pd.Series, new_mask: pd.Series) -> pd.Series:
        """
        Combina máscaras asegurando alineación por índice.
        """
        if new_mask is None:
            return base_mask

        new_mask = new_mask.reindex(base_mask.index, fill_value=False)

        return base_mask | new_mask

    def _get_invalid_indices(self, mask: pd.Series) -> list[int]:
        """
        Extrae índices True de una máscara.
        """
        if mask is None:
            return []

        return mask[mask].index.tolist()
