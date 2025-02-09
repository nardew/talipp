# Timeframe auto-sampling

Timeframe auto-sampling is a special feature intended for indicators working with [OHLCV][talipp.ohlcv.OHLCV] input. By default, indicators add a new output value for each input one. With timeframe auto-sampling it is possible to "merge" several values received within selected timeframe and keep only the last one in given timeframe. This feature suits well e.g. real-time applications which receive new inputs tens or hundreds times a second but the indicators need to be built on sampled timeframe (secondly, minutely, ...).

Supported timeframes are available in [SamplingPeriodType][talipp.input.SamplingPeriodType] enum and include values such as

- [1 second][talipp.input.SamplingPeriodType.SEC_1]
- [3 seconds][talipp.input.SamplingPeriodType.SEC_3]
- [5 seconds][talipp.input.SamplingPeriodType.SEC_5]
- [30 seconds][talipp.input.SamplingPeriodType.SEC_30]
- [1 minute][talipp.input.SamplingPeriodType.MIN_1]
- ...

To enable auto-sampling, setup `input_sampling` attribute when initializing an indicator:

```python
from datetime import datetime
from talipp.indicators import OBV
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV

# choose auto-sampling by 15 seconds
obv = OBV(input_sampling=SamplingPeriodType.SEC_15)

dt = datetime(2024, 1, 1, 0, 0, 0)
ohlcv = OHLCV(1, 1, 1, 1, 1, dt)

# time 00:00:00
obv.add(ohlcv)
print(len(obv)) # 1

# time 00:00:13
ohlcv.time = dt.replace(second=13)
obv.add(ohlcv) # still within the same timeframe => no new value added, the last one updated
print(len(obv)) # 1

# time 00:00:17
ohlcv.time = dt.replace(second=17)
obv.add(ohlcv) # next period entered => new value added
print(len(obv)) # 2

# time 00:00:25
ohlcv.time = dt.replace(second=25)
obv.add(ohlcv) # still within the same timeframe => no new value added, the last one updated
print(len(obv)) # 2
```

!!! tip

    If you want to apply auto-sampling to an indicator which accepts `float` input, e.g. [MACD][talipp.indicators.MACD] indicator, then wrap each input value in a "dummy" [OHLCV][talipp.ohlcv.OHLCV] object, populate its `close` and `time` components and finally provide [input modifier](indicator-chaining.md#input-modifiers) to extract the value

    !!! example

        ```python
        from datetime import datetime
        from talipp.indicators import MACD
        from talipp.input import SamplingPeriodType
        from talipp.ohlcv import OHLCV

        input_floats = [1.0, 2.0, ...]
        dt = datetime(2024, 1, 1, 0, 0, 0)
        input_ohlcv = [OHLCV(None, None, None, value, None, dt) for value in input_floats]
        macd = MACD(input_values=input_ohlcv, input_modifier=lambda x: x.close, input_sampling=SamplingPeriodType.SEC_15)
        ```
