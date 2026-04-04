from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    rule_name: str
    is_valid: bool
    errors: List[str]
    severity: str = "error"
