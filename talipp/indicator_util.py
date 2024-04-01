"""Indicator utilities."""

from __future__ import annotations

from dataclasses import is_dataclass, fields
from typing import Dict, List, Union, Any, TYPE_CHECKING

from talipp.exceptions import TalippException

if TYPE_CHECKING:
    from talipp.indicators.Indicator import Indicator


def has_valid_values(sequence: Union[Indicator, List[Any]], window: int = 1, exact: bool = False) -> bool:
    """Evaluate whether sequence has well-defined values.

    By well-defined values it is meant that the sequence has sufficient length (defined by `window` argument) and its values do not contain `None`. Not all values within the `window` are checked, only the one at the beginning of the window. If it is non-`None`, then it is assumed all values are non-`None`.

    If exact check is required (`exact` argument), then any other value before the window must be `None`.

    Examples:

         sequence=[1, 2], window=2, exact=True/False => return True
         sequence=[1, 2], window=1, exact=False => return True
         sequence=[1, 2], window=1, exact=True => return False
         sequence=[None, 2], window=1, exact=True => return True
         sequence=[None, 2], window=2, exact=True/False => return False

    Args:
        sequence: The input sequence.
        window: The window of values to be evaluated.
        exact: True if the evaluation requires the specified window contains well-defined values but any other greater window does not.

    Returns:
        True if sequence contains well-defined values, otherwise False.
    """
    if not exact:
        return len(sequence) >= window and sequence[-window] is not None
    else:
        return (len(sequence) == window and sequence[-window] is not None) or \
            (len(sequence) > window and sequence[-window] is not None and sequence[-window-1] is None)


def previous_if_exists(sequence: Union[Indicator, List[Any]], index: int = -1, default: Any = 0) -> Any:
    """Return value from `index`th position in the `sequence` if exists, otherwise return `default` value.

    Args:
        sequence: The input sequence.
        index: Index to be returned.
        default: Default value to be returned if `index` is out of range.

    Returns:
        The value from the sequence at `index` position if exists, `default` otherwise.
    """
    try:
        return sequence[index]
    except IndexError:
        return default


def composite_to_lists(indicator: Indicator) -> Dict[str, List[float]]:
    """Transform the list of composite indicator output values into lists of values per each member attribute.

    Applicable only to indicators retuning composite output values.

    Examples:
        Take [Bollinger Bands][talipp.indicators.BB] indicator and its [BBVal][talipp.indicators.BB.BBVal] output value type. If the indicator is printed, it will return

            [BBVal(lb=x1, cb=y1, ub=z1), BBVal(lb=x2, cb=y2, ub=z2), ...]

        If the indicator is passed into `composite_to_lists` method, the output will be transformed into

            {'lb': [x1, x2, ...], 'cb': [y1, y2, ...], 'ub': [z1, z2, ...]}

    Args:
        indicator: Indicator to be transformed.

    Returns:
        A dictionary with keys being all members of the composite output type and values being all indicator's output values of given key.

    Raises:
        TalippException: Indicator returning non-composite output values was passed in.
    """
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
            raise TalippException(f"composite_to_lists(...) method can be used only with indicators returning composite output values, "
                                  f"this indicator returns {indicator.get_output_value_type()}.")
