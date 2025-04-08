from talipp.indicators.IndicatorFactory import IndicatorFactory


"""
Intraday Range

Input type: [OHLCV][talipp.ohlcv.OHLCV]

Output type: `float` (as absolute value)

Args:
    input_values: List of input values.
    input_indicator: Input indicator.
    input_modifier: Input modifier.
    input_sampling: Input sampling type.
"""
IR = IndicatorFactory.get_function_caller(lambda input: input.high - input.low)


"""
Relative Intraday Range

Input type: [OHLCV][talipp.ohlcv.OHLCV]

Output type: `float` (as relative value between 0 and 1)

Args:
    input_values: List of input values.
    input_indicator: Input indicator.
    input_modifier: Input modifier.
    input_sampling: Input sampling type.
"""
RIR = IndicatorFactory.get_function_caller(lambda input: (input.high - input.low) / input.open)
