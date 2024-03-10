# Indicator operations

Each indicator provides operations to read, add, update and remove its values.

## Reading values

Indicators implement [Sequence][collections.abc.Sequence] interface, meaning they can be treated as any other list when reading data.

Following operations demonstrate how to read indicator's values:

```python
from talipp.indicators import SMA

sma = SMA(period=3, input_values=[1,2,3])

# print all values
# outputs [None, None, 2]
print(sma)

# print last value
# outputs 2
print(sma[-1])

# print number of values
# outputs 3
print(len(sma))
```

## Adding values

To incrementally add a new value use [add][talipp.indicators.Indicator.Indicator.add] method:

```python
from talipp.indicators import SMA

sma = SMA(period=3, input_values=[1,2,3])

# add a single value
sma.add(4)

# add a list of values
sma.add([4, 5, 6])
```

## Updating values

To update **the most recent** value use [update][talipp.indicators.Indicator.Indicator.update] method:

```python
from talipp.indicators import SMA

sma = SMA(period=3, input_values=[1,2,3])

# update the last input value
sma.update(4)
```

!!! note

    Update of a value does not change number of indicator's values. Instead, it first removes the last input value and then it appends a new one.

## Removing values

Indicators provide several ways how to remove data:

1. To remove the most recent input value, use [remove][talipp.indicators.Indicator.Indicator.remove] method:
    ```python
    from talipp.indicators import SMA
    
    sma = SMA(period=3, input_values=[1,2,3])
   
    # outputs [None, None, 2]
    print(sma)
    
    # remove the last input value
    sma.remove()
   
    # outputs [None, None]
    print(sma)
    ```

1. To remove all input values, use [remove_all][talipp.indicators.Indicator.Indicator.remove_all] method:
   ```python
   from talipp.indicators import SMA
   
   sma = SMA(period=3, input_values=[1,2,3])
   
   # remove all input values
   sma.remove_all()
   
   # outputs []
   print(sma)
   ```

1. To remove **the oldest** values, use [purge_oldest][talipp.indicators.Indicator.Indicator.purge_oldest] method:
   ```python
   from talipp.indicators import SMA
   
   sma = SMA(period=3, input_values=[1,2,3])
   
   # outputs [None, None, 2]
   print(sma)
   
   # purge the first value
   sma.purge_oldest(1)
   
   # outputs [None, 2]
   print(sma)
   ```

!!! note

    Purging old values is useful when memory consumption is a concern. If old indicator's values are not needed anymore, feel free to purge them. However, be careful not to purge any data if calculation of the current values still depends on them.
