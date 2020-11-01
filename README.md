# TALIpp - Incremental Technical Analysis Library

![](https://img.shields.io/badge/python-3.6-blue.svg) ![](https://img.shields.io/badge/python-3.7-blue.svg) ![](https://img.shields.io/badge/python-3.8-blue.svg) ![](https://img.shields.io/badge/python-3.9-blue.svg) ![](https://img.shields.io/badge/pypy-3-blue.svg) 

`talipp` (or `tali++`) is a Python library implementing financial indicators for technical analysis. The distinctive feature of the library is its incremental computation which fits extremely well real-time applications or applications with iterative input in general.  

Unlike existing libraries for technical analysis which typically have to work on the whole input vector in order to calculate new values of indicators, `talipp` due to its incremental architecture calculates new indicators' values exclusively based on the delta input data. That implies, among others, it requires `O(1)` time to produce new values in comparison to `O(n)` (or worse) required by other libraries.

Supported incremental operations include:

- appending new values to the input
- updating the last input value
- removing arbitrary number of the input values

Besides the already mentioned superior time complexity for delta input operations, `talipp`'s incremental approach immediately offers other interesting features for free, such as indicator chaining or building new indicators combined from other indicators. See section with examples to get an idea.

Incremental nature of `talipp` naturally excels in applications with frequent `CUD` operations but it can be used for charting, back-testing, ... as any other existing library.

Last but not least, `talipp` is a very young project and therefore open to any suggestions of amending the API to users' liking. You are encouraged to come up with proposals.

---

### What's new in version 1.1.0

- indicator chaining
- delta input values can be added as a single values as well as a list

For the full history of changes see [CHANGELOG](https://github.com/nardew/talipp/blob/master/CHANGELOG.md).

---

### List of incremental indicators

`talipp` currently provides below set of indicators. If your favourite indicator is missing, then create a ticket via GitHub Issues and there is a chance that it will be included in the future version of the library.

| Type | Indicators |
| :---: | --- |
| **trend** | Average Directional Index (ADX) <br> Awesome Oscillator (AO) <br> Ichimoku Kinko Hyo <br> Know Sure Thing (KST) <br> Moving Average Convergence Divergence (MACD) <br> Mass Index <br> Moving Average (ALMA, SMA, SMMA, DEMA, EMA, HMA, TEMA, VWMA, WMA) <br> Parabolic SAR <br> SFX TOR
| **support/resistance** | High/Low Pivots
| **momentum** | Chaikin Oscillator <br> Rate of Change (ROC) <br> Relative strength index (RSI) <br> Stochastic Oscillator <br> Stochastic RSI <br> Ultimate Oscillator (UO)
| **volume** | Accumulation/Distribution (ADL) <br> On-balance Volume (OBV)
| **volatility** | Average True Range (ATR) <br> Bollinger Bands (BB) <br> Donchian Channel (DC) <br> Keltner Channel (KC) <br> Standard deviation

### Installation
```bash
pip install talipp
```
In case you want to install the latest version from the repo, use
```bash
pip install git+https://github.com/nardew/talipp.git@master
```

### Examples

Consult `examples` folder to see usage of every single indicator included in the library. To get the basic look and feel of the API, see below. 

```python
from talipp.indicators import EMA, Stoch
from talipp.ohlcv import OHLCVFactory

# EMA indicator ([float] -> [float])
ema = EMA(period = 3, input_values = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10])

# treat indicators as any other list
print(f'EMA(3): {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125]
print(f'Last EMA value: {ema[-1]}') # 8.28125

# append a new input value incrementally
ema.add_input_value(11)
print(f'EMA after adding a new value:      {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125, 9.640625]

# change the last added value
ema.update_input_value(15)
print(f'EMA after updating the last value: {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125, 11.640625]

# change the last added value again
ema.update_input_value(18)
print(f'EMA after updating the last value: {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125, 13.140625]

# remove the last added value
ema.remove_input_value()
print(f'EMA after removing the last value: {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125]

# STOCH indicator ([OHLCV] -> [composite])
stoch = Stoch(5, 3, OHLCVFactory.from_dict({
    'high':     [5, 10, 15, 20, 25, 30, 35],
    'low':      [1, 4, 7, 10, 13, 16, 19],
    'close':    [3, 9, 8, 19, 18, 17, 19]
}))

# print result as a list of composite values for 'k' and 'd' output parameters
print(f'Stoch(5, 3) composite result: {stoch}') # [StochVal(k=70.83333333333333, d=None), StochVal(k=50.0, d=None), StochVal(k=42.857142857142854, d=54.563492063492056)]

# print result as lists per output parameters
print(f'Stoch(5, 3) decomposed result: {stoch.to_lists()}') # {'k': [70.83333333333333, 50.0, 42.857142857142854], 'd': [None, None, 54.563492063492056]} 

# Indicator chaining
sma1 = SMA(3)
sma2 = SMA(3, input_indicator = sma1)
sma3 = SMA(3, input_indicator = sma2)

sma1.add_input_value([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"SMA1: {sma1}") # [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
print(f"SMA2: {sma2}") # [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
print(f"SMA3: {sma3}") # [4.0, 5.0, 6.0, 7.0]
```

### Contact

- to report issues, bugs, corrections or to propose new features use preferably Github Issues
- for topics requiring more personal approach feel free to send an e-mail to <img src="http://safemail.justlikeed.net/e/581536c5ad7cf046df49d5e52452cb20.png" border="0" align="absbottom">

### Support

If you like the library and you feel like you want to support its further development, enhancements and bug fixing, then it will be of great help and most appreciated if you:
- file bugs, proposals, pull requests, ...
- spread the word
- donate an arbitrary tip
  * `BTC`: `3GJPT6H6WeuTWR2KwDSEN5qyJq95LEErzf`
  * `ETH`: `0xC7d8673Ee1B01f6F10e40aA416a1b0A746eaBe68`
