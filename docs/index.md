# Home

![python](https://img.shields.io/pypi/pyversions/talipp?logo=python)
![PyPy](https://img.shields.io/badge/pypy-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)
![GitHub Release Date](https://img.shields.io/github/release-date/nardew/talipp?logo=pypi)
![pypi](https://img.shields.io/pypi/l/talipp)


**talipp** (a.k.a. **tali++**) is a Python library implementing [financial indicators](indicator-catalogue.md) for technical analysis. The distinctive feature of the library is its _incremental computation_ which fits well real-time applications or applications with iterative input in general.  

Supported incremental operations are:

- **adding** a new input value
- **updating** the last input value
- **removing** input values

``` py title="example"
from talipp.indicators import SMA

# initialize standard moving average with period of 3
sma = SMA(period = 3, input_values = [1, 2, 3, 4])

# print indicator
print(f'SMA(3): {sma}') # [None, None, 2.0, 3.0]

# append a new input value incrementally
sma.add(5)
print(f'SMA(3): {sma}') # [None, None, 2.0, 3.0, 4.0]

# update the last value
sma.update(8)
print(f'SMA(3): {sma}') # [None, None, 2.0, 3.0, 5.0]

# update the last value again
sma.update(11)
print(f'SMA(3): {sma}') # [None, None, 2.0, 3.0, 6.0]

# remove the last value
sma.remove()
print(f'SMA(3): {sma}') # [None, None, 2.0, 3.0]
```

Incremental nature of the library means that any update of the input data is reflected in the indicators' values in O(1) in contrary to O(n) of standard libraries which need to recalculate *all* indicator values from scratch. 

To give you better perspective about the performance gain look at the below figure. It compares running time of incremental (talipp) and non-incremental (talib) libraries when calculating SMA(20) for inputs of various sizes where input values are fed one by one. 

![SMA(20) comparison](images/sma20-comparison.svg "SMA(20) comparison")
