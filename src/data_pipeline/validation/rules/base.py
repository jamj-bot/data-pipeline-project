from abc import ABC, abstractmethod
from typing import Type
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
    def validate(self, data: pd.DataFrame) -> None:
        pass

