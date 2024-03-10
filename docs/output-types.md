# Output types

Like indicators that process either simple or complex input values, the output values of indicators can also range from simple floats to complex objects.

Complex output types are required if indicator needs to return multiple values per a single data point. For instance, while [SMA][talipp.indicators.SMA] will always return a single output value for each input value, [Bollinger Bands][talipp.indicators.BB.BB] has to return three values per each input value (lower, central and upper band), hence requiring a complex return type.

Complex output type is always defined as a `dataclass` and is documented in each indicator module.

For instance, output type of [Bollinger Bands][talipp.indicators.BB.BB] is [BBVal][talipp.indicators.BB.BBVal] and looks as follows:

```python
@dataclass
class BBVal:
    lb: float = None
    cb: float = None
    ub: float = None
```

That's why when printing [Bollinger Bands][talipp.indicators.BB.BB], the output will be

```commandline
[BBVal(...), BBVal(...), BBVal(...), ...]
```

Other examples of complex output types are:

* [MACD][talipp.indicators.MACD.MACD] -> [MACDVal][talipp.indicators.MACD.MACDVal]
* [Parabolic SAR][talipp.indicators.ParabolicSAR.ParabolicSAR] -> [ParabolicSARVal][talipp.indicators.ParabolicSAR.ParabolicSARVal]
* [Stoch][talipp.indicators.Stoch.Stoch] -> [StochVal][talipp.indicators.Stoch.StochVal]
* ...

When complex outputs serve as an input for other components in a data pipeline sometimes it may be more convenient to decompose them into lists per each attribute of the complex type. In other words, instead of working with

```python
[StochVal(k=10, d=None), StochVal(k=20.0, d=15), StochVal(k=12, d=14)]
```

it may be more useful to have

```python
{
    'k': [  10, 20, 12], 
    'd': [None, 15, 14]
}
```

To transform the former output into the latter, talipp provides [composite_to_lists][talipp.indicator_util.composite_to_lists] utility function which can be applied to every indicator returning complex types.
