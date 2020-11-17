from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType


class McGinleyDynamic(Indicator):
    """
    McGinley Dynamic

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period:
            return None
        elif len(self.input_values) == self.period:
            return sum(self.input_values) / float(self.period)
        else:
            print(self.output_values[-1])
            print(pow(self.input_values[-1] / float(self.output_values[-1]), 4))
            print(self.input_values[-1])
            print(self.output_values[-1])
            return self.output_values[-1] + (self.input_values[-1] - self.output_values[-1]) / float(self.period * pow(self.input_values[-1] / float(self.output_values[-1]), 4))