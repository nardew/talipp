# Input types

Indicators work with two types of input data - simple `float` or complex [OHLCV][talipp.ohlcv.OHLCV] objects. While `float` is used in indicators requiring just a plain series of numbers, `OHLCV` object provides additional data (open, high, low, close price and optional volume and time) needed by certain class of indicators.

Each indicator defines what kind of input it requires. It can be derived either from the type of `input_values` parameter present in the indicator's `__init__` method or from the indicator's documentation.

To make conversion from user's format of input data into `OHLCV` objects easy talipp provides [OHLCVFactory][talipp.ohlcv.OHLCVFactory] helper class.
