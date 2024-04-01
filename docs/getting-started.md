# Getting started

## Installation

talipp can be installed from the following sources:

##### :simple-pypi:&nbsp; PyPI

```bash
pip install talipp
```
##### :simple-github:&nbsp; GitHub

```bash
pip install git+https://github.com/nardew/talipp.git@main
```

##### :simple-condaforge:&nbsp; Conda

```bash
conda install conda-forge::talipp
```

## Essentials

### Import indicators

Indicators can be imported as

```python
from talipp.indicators import <indicator_name>
```

For instance, to import [EMA][talipp.indicators.EMA.EMA] indicator, use

```python
from talipp.indicators import EMA
```

List of all indicators can be found in the [Indicator catalogue](indicator-catalogue.md).

### Basic usage

Indicators can be fed input values either during their initialization

```python
from talipp.indicators import EMA

ema = EMA(period=3, input_values=[1, 2, 3, 4, 5])
```

or incrementally

```python
from talipp.indicators import EMA

ema = EMA(period=3)
ema.add(1)
ema.add(2)
...
```

To print indicator's values you can treat each indicator as a list, i.e. you can do

```python
from talipp.indicators import EMA

ema = EMA(period=3, input_values=[1, 2, 3, 4, 5])

print(ema[-1])
print(ema[-5:])
print(ema)
```

Detailed description of indicator manipulation can be found in the section [Indicator operations](indicator-operations.md).

### Input types

Indicators can accept two types of input - simple type such as `float` or complex [OHLCV][talipp.ohlcv.OHLCV] type encapsulating structured data such as open price, high price, low price, close price, ... 

Each indicator specifies what type of input is required. For instance, [SMA][talipp.indicators.SMA.SMA] indicator accepts `float` while [Stoch][talipp.indicators.Stoch.Stoch] indicator accepts `OHLCV`.

```python
from talipp.indicators import SMA, Stoch
from talipp.ohlcv import OHLCV

sma = SMA(period=3, input_values=[1, 2, 3])
stoch = Stoch(period=3, smoothing_period=2, input_values=[OHLCV(1, 2, 3, 4), OHLCV(5, 6, 7, 8)])
```

Read more about input types in the [Input types](input-types.md) section.

## Examples

The library comes with [examples](https://github.com/nardew/talipp/blob/main/examples/indicators.py) showcasing usage of each indicator on artificial input.

If you have a binance account, then you can check [examples](https://github.com/nardew/talipp/blob/main/examples/binance_online.py) of indicators on realtime data. 
