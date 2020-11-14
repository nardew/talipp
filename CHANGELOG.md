# Changelog

All notable changes to this project will be documented in this file.

The project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Pending release]

## [1.4.0] - 2020-11-14

- new indicators: Detrended Price Oscillator (DPO), Ease of Movement (EMV), Klinger Volume Oscillator (KVO), Vortex Indicator (VTX) 

## [1.3.0] - 2020-11-06

- new indicators: Chande Kroll Stop, Choppiness Index, Commodity Channel Index, Coppock Curve, Mean Deviation
- performance comparison with `talib` library

## [1.2.0] - 2020-11-04

- new indicators: Aroon, Balance of Power (BOP), KAMA, TSI, TRIX

## [1.1.0] - 2020-11-01

- indicator chaining (see the example in README)

  ```python
  sma = SMA(15, input_indicator = SMA(10, input_indicator = SMA(5, [1, 2, 3, ...])))
  ```

- delta input values can be added as a single values as well as a list

  ```python
  sma.add_input_value(5)
  sma.add_input_value([5, 6, 7])
  ```

## 1.0.0 - 2020-10-28

- the official release of `talipp`

[Pending release]: https://github.com/nardew/talipp/compare/1.4.0...HEAD
[1.4.0]: https://github.com/nardew/talipp/compare/1.3.0...1.4.0
[1.3.0]: https://github.com/nardew/talipp/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/nardew/talipp/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/nardew/talipp/compare/1.0.0...1.1.0