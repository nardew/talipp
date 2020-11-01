from typing import List, Any

from talipp.indicators.Indicator import Indicator


class RSI(Indicator):
    """
    Relative Strength Index

    Output: a list of floats
    """
    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.period = period

        self.avg_gain = []
        self.avg_loss = []

        self.add_managed_sequence(self.avg_gain)
        self.add_managed_sequence(self.avg_loss)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period + 1:
            return None
        elif len(self.input_values) == self.period + 1:
            # calculate initial changes in price
            init_changes = [self.input_values[i] - self.input_values[i - 1] for i in range(1, self.period)]

            # initialize average gain and loss
            self.avg_gain.append(float(sum(init_changes[i] for i in range(len(init_changes)) if init_changes[i] > 0)) / (self.period - 1))
            self.avg_loss.append(float(sum(-1 * init_changes[i] for i in range(len(init_changes)) if init_changes[i] < 0)) / (self.period - 1))

        change = self.input_values[-1] - self.input_values[-2]

        gain = change if change > 0 else 0.0
        loss = -1 * change if change < 0 else 0.0

        self.avg_gain.append(float(self.avg_gain[-1] * (self.period - 1) + gain) / self.period)
        self.avg_loss.append(float(self.avg_loss[-1] * (self.period - 1) + loss) / self.period)

        if self.avg_loss[-1] == 0:
            rsi = 100.0
        else:
            rs = self.avg_gain[-1] / self.avg_loss[-1]
            rsi = 100.0 - (100.0 / (1.0 + rs))

        return rsi
