from talipp.indicator_util import composite_to_lists
from talipp.indicators import EMA, SMA, Stoch
from talipp.ohlcv import OHLCVFactory

# EMA indicator ([float] -> [float])
ema = EMA(period = 3, input_values = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10])

# treat indicators as any other list
print(f'EMA(3): {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125]
print(f'Last EMA value: {ema[-1]}') # 8.28125

# append a new input value in the incrementally
ema.add(11)
print(f'EMA after adding a new value:      {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125, 9.640625]

# change the last added value
ema.update(15)
print(f'EMA after updating the last value: {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125, 11.640625]

# change the last added value again
ema.update(18)
print(f'EMA after updating the last value: {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125, 13.140625]

# remove the last added value
ema.remove()
print(f'EMA after removing the last value: {ema}') # [3.0, 5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125]

# purge the oldest input value
ema.purge_oldest(1)
print(f'EMA after purging the oldest value: {ema}') # [5.0, 7.0, 4.5, 4.25, 5.125, 6.5625, 8.28125]

# STOCH indicator ([OHLCV] -> [composite])
stoch = Stoch(5, 3, OHLCVFactory.from_dict({
    'high':     [5, 10, 15, 20, 25, 30, 35],
    'low':      [1, 4, 7, 10, 13, 16, 19],
    'close':    [3, 9, 8, 19, 18, 17, 19]
}))

# print result as a list of composite values for 'k' and 'd' output parameters
print(f'Stoch(5, 3) composite result: {stoch}') # [StochVal(k=70.83333333333333, d=None), StochVal(k=50.0, d=None), StochVal(k=42.857142857142854, d=54.563492063492056)]

# print result as lists per output parameters
print(f'Stoch(5, 3) decomposed result: {composite_to_lists(stoch)}') # {'k': [70.83333333333333, 50.0, 42.857142857142854], 'd': [None, None, 54.563492063492056]}

# Indicator chaining
sma1 = SMA(3)
sma2 = SMA(3, input_indicator = sma1)
sma3 = SMA(3, input_indicator = sma2)

print(f"Chain three moving averages:")
sma1.add([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"SMA1: {sma1}") # [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
print(f"SMA2: {sma2}") # [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
print(f"SMA3: {sma3}") # [4.0, 5.0, 6.0, 7.0]

print(f"Purge oldest 3 values:")
sma1.purge_oldest(3)
print(f"SMA1: {sma1}") # [5.0, 6.0, 7.0, 8.0, 9.0]
print(f"SMA2: {sma2}") # [6.0, 7.0, 8.0]
print(f"SMA3: {sma3}") # [7.0]
