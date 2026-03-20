from typing import List
from data_pipeline.validation.rules.schema.required_columns import RequiredColumnsRule
from data_pipeline.validation.rules.schema.column_types import ColumnTypesRule
from data_pipeline.validation.rules.schema.allowed_values import AllowedValuesRule
from data_pipeline.validation.rules.schema.value_range import ValueRangeRule
from data_pipeline.validation.rules.business.numeric_range_rule import NumericRangeRule
from data_pipeline.validation.rules.base import RULE_REGISTRY, ValidationRule


def create_rules(config: list[dict]) -> List[ValidationRule]:

    rules: List[ValidationRule] = []

    for rule_cfg in config:

        rule_type = rule_cfg.get("type")

        if not rule_type:
            raise ValueError("Cada regla debe tener 'type'")

        if rule_type not in RULE_REGISTRY:
            raise ValueError(f"Regla no registrada: {rule_type}")

        rule_class = RULE_REGISTRY[rule_type]

        params = {k: v for k, v in rule_cfg.items() if k != "type"}

        rules.append(rule_class(**params))

    return rules
