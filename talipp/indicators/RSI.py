from typing import List, Any

from talipp.indicators.Indicator import Indicator


class RSI(Indicator):
    """
    Relative Strength Index

    Output: a list of floats
    """
    def __init__(self, period: int, input_values: List[float] = None):
        super().__init__()

        self.period = period

        self.last_avg_gain = 0.0
        self.last_avg_loss = 0.0
        self.prev_last_avg_gain = 0.0
        self.prev_last_avg_loss = 0.0

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        self.prev_last_avg_gain = self.last_avg_gain
        self.prev_last_avg_loss = self.last_avg_loss

        if len(self.input_values) < self.period + 1:
            return None
        elif len(self.input_values) == self.period + 1:
            # calculate initial changes in price
            init_changes = [self.input_values[i] - self.input_values[i - 1] for i in range(1, self.period)]

            # initialize average gain and loss
            self.last_avg_gain = float(sum(init_changes[i] for i in range(len(init_changes)) if init_changes[i] > 0)) / (self.period - 1)
            self.last_avg_loss = float(sum(-1 * init_changes[i] for i in range(len(init_changes)) if init_changes[i] < 0)) / (self.period - 1)

        change = self.input_values[-1] - self.input_values[-2]

        gain = change if change > 0 else 0.0
        loss = -1 * change if change < 0 else 0.0

        self.last_avg_gain = float(self.last_avg_gain * (self.period - 1) + gain) / self.period
        self.last_avg_loss = float(self.last_avg_loss * (self.period - 1) + loss) / self.period

        if self.last_avg_loss == 0:
            rsi = 100.0
        else:
            rs = self.last_avg_gain / self.last_avg_loss
            rsi = 100.0 - (100.0 / (1.0 + rs))

        return rsi

    def _remove_input_value_custom(self) -> None:
        self.last_avg_gain = self.prev_last_avg_gain
        self.last_avg_loss = self.prev_last_avg_loss

    def _remove_all_custom(self) -> None:
        self.last_avg_gain = 0.0
        self.last_avg_loss = 0.0
        self.prev_last_avg_gain = 0.0
        self.prev_last_avg_loss = 0.0