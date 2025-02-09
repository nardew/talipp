# Indicator chaining

talipp offers a unique feature of chaining multiple indicators into a pipeline. When indicators are chained, each output of one indicator immediately becomes a new input of the one after forming a train of propagating values. As always, all this in constant time!

The major benefit of chaining indicators is it allows user to define their custom indicators. To chain indicators, one links them together via `input_indicator` parameter during initialization as illustrated below. Notice how the second indicator produces new outputs even without any explicit calls of `add` method:

```python
from talipp.indicators import SMA

sma1 = SMA(2)
sma2 = SMA(2, input_indicator = sma1)

sma1.add(1)
print(f"SMA1: {sma1}") # [None]
print(f"SMA2: {sma2}") # [None]

sma1.add(2)
print(f"SMA1: {sma1}") # [None, 1.5]
print(f"SMA2: {sma2}") # [None, None]

sma1.add(3)
print(f"SMA1: {sma1}") # [None, 1.5,  2.5]
print(f"SMA2: {sma2}") # [None, None, 2]
```

One typical use-case of indicator chaining is to produce a smoothed version of an existing indicator:

```python
from talipp.indicators import SMA, RSI

rsi = RSI(14)
smoothed_rsi = SMA(9, input_indicator = rsi)

rsi.add([...])
print(smoothed_rsi)
```

There is no limit to the number of chained indicators, one can create a computation pipeline from as many indicators as needed.

## Input modifiers

Chaining of indicators assumes that output and input types of chained indicators match. In case they do not, talipp provides an option to specify a conversion function which will be applied to the output value before it is fed to the next indicator. The function is specified in indicator's `__init__` method via `input_modifier` attribute.

To illustrate usage of input modifiers, imagine we want to create a new indicator based on [Bollinger Bands][talipp.indicators.BB.BB] which will calculate [EMA][talipp.indicators.EMA.EMA] of the upper band. With standard libraries you would first calculate `Bolliger Bands`, then extract the upper band and finally feed it to `EMA`. With indicator chaining we can do better (besides it gives much more efficient solution). The only issue is that while `EMA` expects `floats` as the input, `Bollinger Bands` produce [BBVal][talipp.indicators.BB.BBVal]. Input modifiers for the rescue.

```python
from talipp.indicators import BB, EMA

bb = BB(5, 2)
ema_bb = EMA(3, input_indicator=bb, input_modifier=lambda x: x.ub)
```
