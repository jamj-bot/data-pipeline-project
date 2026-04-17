from dataclasses import dataclass, field
from typing import List


@dataclass
class ValidationResult:
    """
    Representa el resultado de una regla de validación.

    Tipos de reglas:

    1. Dataset-level (estructurales)
        - is_row_level = False
        - invalid_rows = []

    2. Row-level
        - is_row_level = True
        - invalid_rows contiene índices inválidos
    """

    rule_name: str
    is_valid: bool
    errors: List[str]
    severity: str = "error"

    is_row_level: bool = False

    invalid_rows: List[int] = field(default_factory=list)
