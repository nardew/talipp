from __future__ import annotations

from dataclasses import is_dataclass, fields
from typing import Dict, List, Union, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from talipp.indicators.Indicator import Indicator


def has_valid_values(sequence: Union[Indicator, List[Any]], window: int = 1, exact: bool = False) -> bool:
    if not exact:
        return len(sequence) >= window and sequence[-window] is not None
    else:
        return (len(sequence) == window and sequence[-window] is not None) or \
            (len(sequence) > window and sequence[-window] is not None and sequence[-window-1] is None)


def composite_to_lists(indicator: Indicator) -> Dict[str, List[float]]:
    if not has_valid_values(indicator, 1):
        return {}
    else:
        if is_dataclass(indicator.get_output_value_type()):
            result = {key: [] for key in map(lambda x: x.name, fields(indicator.get_output_value_type()))}
            for output_value in indicator:
                for key in fields(indicator.get_output_value_type()):
                    if output_value is not None:
                        result[key.name].append(output_value.__dict__[key.name])
                    else:
                        result[key.name].append(None)
            return result
        else:
            raise Exception(f"composite_to_lists() method can be used only with indicators returning composite output values, "
                            f"this indicator returns {indicator.get_output_value_type()}.")
