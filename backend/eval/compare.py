from pydantic import BaseModel
from typing import Any

from app.schemas.invoice_schema import InvoiceFields

def compare_documents(predicted: BaseModel, golden: BaseModel) -> dict[str, bool]: 
    results: dict[str, bool] = {}

    for field_name in InvoiceFields.model_fields: 
        predicted_value = getattr(predicted, field_name, None)
        golden_value = getattr(golden, field_name, None)

        if predicted_value is None and golden_value is None:
            continue

        results[field_name] = _values_match(predicted_value, golden_value)

    return results 

def _values_match(predicted_value: Any, golden_value: Any) -> bool:
    # One side present, other absent -> mismatch (hallucinated response)
    if (predicted_value is None) != (golden_value is None):
        return False

    # Float: tolearance-based comparison
    if isinstance(golden_value, float) and isinstance(predicted_value, float):
        return abs(predicted_value - golden_value) <= max(0.01, abs(golden_value) * 0.01)

    # Nested pydantic model: recurse, and treat as a match only if all sub-fields match
    if isinstance(golden_value, BaseModel) and isinstance(predicted_value, BaseModel):
        sub_result = compare_documents(predicted_value, golden_value)
        return all(sub_result.values()) if sub_result else True

    # List of nested pydantic models: postion based comparison
    if(
        isinstance(golden_value, list)
        and golden_value
        and isinstance(golden_value[0], BaseModel)
    ):
        if len(predicted_value) != len(golden_value):
            return False
        return all(
            all(compare_documents(p_item, g_item).values()) if compare_documents(p_item, g_item) else True
            for p_item, g_item in zip(predicted_value, golden_value)
        )

    #Everything else(str, int, plain lists, bool): exact equality
    return predicted_value == golden_value