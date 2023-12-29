from abc import ABCMeta, abstractmethod
from collections.abc import MutableSequence, Sequence
from warnings import warn
from typing import List, Any, Callable, Union, Type

ListAny = List[Any]
ManagedSequenceType = Union['Indicator', MutableSequence]
InputModifierType = Callable[..., Any]


class Indicator(Sequence):
    __metaclass__ = ABCMeta

    def __init__(self, input_modifier: InputModifierType = None, output_value_type: Type = float):
        self.input_modifier =input_modifier
        self.output_value_type = output_value_type

        self.input_values: ListAny = []
        self.output_values: ListAny = []
        self.managed_sequences: List[ManagedSequenceType] = []
        self.sub_indicators: List[Indicator] = []
        self.output_listeners: List[Indicator] = []

    @abstractmethod
    def _calculate_new_value(self) -> Any:
        pass

    def __getitem__(self, index):
        return self.output_values[index]

    def __len__(self):
        return len(self.output_values)

    def __str__(self):
        return str(self.output_values)

    def add_sub_indicator(self, indicator: 'Indicator') -> None:
        self.sub_indicators.append(indicator)

    def add_managed_sequence(self, lst: ManagedSequenceType) -> None:
        self.managed_sequences.append(lst)

    def initialize(self, input_values: ListAny = None, input_indicator: 'Indicator' = None) -> None:
        if input_values is not None and input_indicator is not None:
            raise Exception('Indicator cannot be initialized with both input_values and input_indicator!')

        self.remove_all()

        if input_values is not None:
            for value in input_values:
                self.add(value)

        if input_indicator is not None:
            for value in input_indicator:
                self.add(value)

            input_indicator.add_output_listener(self)

    def add_input_value(self, value: Any) -> None:
        warn('This method is deprecated and will be removed in the next major version. '
             'Please use add(...) method with the same signature instead.',
             DeprecationWarning,
             stacklevel=2)
        return self.add(value)

    def add(self, value: Any) -> None:
        for sub_indicator in self.sub_indicators:
            sub_indicator.add(value)

        if not isinstance(value, list):
            value = [value]

        for input_value in value:
            if input_value is not None and self.input_modifier is not None:
                input_value = self.input_modifier(input_value)
            self.input_values.append(input_value)

            if input_value is not None:
                new_value = self._calculate_new_value()
            else:
                new_value = None

            if new_value is None and len(self.output_values) > 0:
                new_value = self.output_values[-1]

            self._add_to_output_values(new_value)

            for listener in self.output_listeners:
                listener.add(new_value)

    def update_input_value(self, value: Any) -> None:
        warn('This method is deprecated and will be removed in the next major version. '
             'Please use update(...) method with the same signature instead.',
             DeprecationWarning,
             stacklevel=2)
        return self.update(value)

    def update(self, value: Any) -> None:
        self.remove()
        self.add(value)

    def remove_input_value(self) -> None:
        warn('This method is deprecated and will be removed in the next major version. '
             'Please use remove(...) method with the same signature instead.',
             DeprecationWarning,
             stacklevel=2)
        return self.remove()

    def remove(self) -> None:
        for sub_indicator in self.sub_indicators:
            sub_indicator.remove()

        if len(self.input_values) > 0:
            self.input_values.pop(-1)

        self._remove_output_value()

        for lst in self.managed_sequences:
            if isinstance(lst, Indicator):
                lst.remove()
            else:
                if len(lst) > 0:
                    lst.pop(-1)

        self._remove_custom()

        for listener in self.output_listeners:
            listener.remove()

    def _add_to_output_values(self, value: Any) -> None:
        self.output_values.append(value)

    def _remove_output_value(self) -> None:
        if len(self.output_values) > 0:
            self.output_values.pop(-1)

    def _remove_custom(self) -> None:
        pass

    def remove_all(self) -> None:
        for sub_indicator in self.sub_indicators:
            sub_indicator.remove_all()

        self.input_values = []
        self.output_values = []

        for lst in self.managed_sequences:
            if isinstance(lst, Indicator):
                lst.remove_all()
            else:
                lst.clear()

        self._remove_all_custom()

        for listener in self.output_listeners:
            listener.remove_all()

    def _remove_all_custom(self) -> None:
        pass

    def purge_oldest(self, size: int) -> None:
        for sub_indicator in self.sub_indicators:
            sub_indicator.purge_oldest(size)

        if len(self.input_values) > 0:
            self.input_values = self.input_values[size:]

        self._purge_oldest_output_value(size)

        for lst in self.managed_sequences:
            if isinstance(lst, Indicator):
                lst.purge_oldest(size)
            else:
                del lst[:size]

        self._purge_oldest_custom(size)

        for listener in self.output_listeners:
            listener.purge_oldest(size)

    def _purge_oldest_output_value(self, size: int) -> None:
        self.output_values = self.output_values[size:]

    def _purge_oldest_custom(self, size: int) -> None:
        pass

    def set_input_values(self, input_values: ListAny, initialize: bool = True) -> None:
        if initialize:
            self.initialize(input_values)
        else:
            self.input_values = input_values

    def add_output_listener(self, listener: 'Indicator') -> None:
        self.output_listeners.append(listener)

    def get_output_value_type(self):
        return self.output_value_type
