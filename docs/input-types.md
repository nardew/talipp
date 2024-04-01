# Input types

Indicators work with two types of input data - simple `float` or complex [OHLCV][talipp.ohlcv.OHLCV] objects. While `float` is used in indicators requiring just a plain series of numbers, `OHLCV` object provides additional data (open, high, low, close price and optional volume and time) needed by certain class of indicators.

Each indicator defines what kind of input it requires. Users can derive it either from the type of `input_values` parameter present in the indicator's `__init__` method or from the indicator's documentation.

Below is an example of one indicator consuming `floats` and another one consuming `OHLCV` objects.

```python
from talipp.indicators import SMA, Stoch
from talipp.ohlcv import OHLCV

sma = SMA(period=3, input_values=[1, 2, 3])
stoch = Stoch(period=3, smoothing_period=2, input_values=[OHLCV(1, 2, 3, 4), OHLCV(5, 6, 7, 8)])
```

## OHLCV factory

To simplify conversion from user's format of input data to `OHLCV` objects, talipp provides [OHLCVFactory][talipp.ohlcv.OHLCVFactory] helper class. The factory offers three static helpers:

### [from_dict][talipp.ohlcv.OHLCVFactory.from_dict]

This method accepts a dictionary with `open`, `high`, `low`, `close` and optionally `volume` and `time` keys where each key contains a list of values and generates a list of `OHLCV` objects out of them.

Example:

```python
from talipp.ohlcv import OHLCVFactory

user_input = {
    'open':  [1,  2,  3],
    'high':  [4,  5,  6],
    'low':   [7,  8,  9],
    'close': [10, 11, 12]
}

print(OHLCVFactory.from_dict(user_input))
```

Output:

```commandline
[OHLCV(1, 4, 7, 10), OHLCV(2, 5, 8, 11), OHLCV(3, 6, 9, 12)]
```

### [from_matrix][talipp.ohlcv.OHLCVFactory.from_matrix]

This method accepts a list of tuples where each tuple represents values to be used in `OHLCV` object.

Example:

```python
from talipp.ohlcv import OHLCVFactory

user_input = [
    (1,  2,  3,  4),
    (5,  6,  7,  8),
    (9, 10, 11, 12)
]

print(OHLCVFactory.from_matrix(user_input))
```

Output:

```commandline
[OHLCV(1, 2, 3, 4), OHLCV(5, 6, 7, 8), OHLCV(9, 10, 11, 12)]
```

### [from_matrix2][talipp.ohlcv.OHLCVFactory.from_matrix2]

Similar to [from_matrix](#from_matrix), this method accepts a list of lists where the first list represents all `open` values, the second represents all `highs`, etc.

```python
from talipp.ohlcv import OHLCVFactory

user_input = [
    [ 1,  2,  3],
    [ 4,  5,  6],
    [ 7,  8,  9],
    [10, 11, 12]
]

print(OHLCVFactory.from_matrix2(user_input))
```

Output:

```commandline
[OHLCV(1, 4, 7, 10), OHLCV(2, 5, 8, 11), OHLCV(3, 6, 9, 12)]
```
