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

    def _get_invalid_indices(self, mask: pd.Series) -> list[int]:
        if mask is None or not mask.any():
            return []
        return mask[mask].index.tolist()

    def _combine_masks(self, base_mask: pd.Series, new_mask: pd.Series) -> pd.Series:
        if new_mask is None:
            return base_mask
        return base_mask | new_mask
