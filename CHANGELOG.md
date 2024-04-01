# Changelog

All notable changes to this project will be documented in this file.

The project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Pending release]

## [2.1.2] - 2024-04-01

- fix `Aroon` indicator arguments

## [2.1.1] - 2024-03-25

- fix division by zero in `ADX`

## [2.1.0] - 2024-03-24

- auto-sampling of input values added

## [2.0.0] - 2024-01-01

- scope: https://github.com/nardew/talipp/issues/111

## [1.10.0] - 2023-12-24

- new `Schaff Trend Cycle` indicator added.

## [1.9.3] - 2023-12-16

- dropped support for python `3.7`

## [1.9.2] - 2023-12-16

- dropped support for python `3.6`
- added support for python `3.10` and `3.11`

## [1.9.1] - 2022-10-01

- conda-forge alignment

## [1.9.0] - 2022-07-07

- new `TTM Squeeze` indicator added.

## [1.8.0] - 2022-06-11

- new `SuperTrend` indicator added.

## [1.7.1] - 2022-05-21

- `TSI` calculation fixed when input contains a long series of identical values (division by zero occurred before). After the fix the indicator will simply copy previous value should division by zero occur.

## [1.7.0] - 2021-08-31

- `OHLCV` class extended with timestamp
- `ATR` calculation of the very first value fixed

## [1.6.0] - 2021-06-14

- new `VWAP` indicator added

## [1.5.0] - 2020-11-23

- a new possibility to purge old data in order to free memory (use `indicator.purge_oldest(purge_size)`)

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
  sma.add(5)
  sma.add([5, 6, 7])
  ```

## 1.0.0 - 2020-10-28

- the official release of `talipp`

[Pending release]: https://github.com/nardew/talipp/compare/2.1.2...HEAD
[2.1.2]: https://github.com/nardew/talipp/releases/tag/2.1.2
[2.1.1]: https://github.com/nardew/talipp/compare/2.1.0...2.1.1
[2.1.0]: https://github.com/nardew/talipp/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/nardew/talipp/compare/1.10.0...2.0.0
[1.10.0]: https://github.com/nardew/talipp/compare/1.9.3...1.10.0
[1.9.3]: https://github.com/nardew/talipp/compare/1.9.2...1.9.3
[1.9.2]: https://github.com/nardew/talipp/compare/1.9.1...1.9.2
[1.9.1]: https://github.com/nardew/talipp/compare/1.9.0...1.9.1
[1.9.0]: https://github.com/nardew/talipp/compare/1.8.0...1.9.0
[1.8.0]: https://github.com/nardew/talipp/compare/1.7.1...1.8.0
[1.7.1]: https://github.com/nardew/talipp/compare/1.7.0...1.7.1
[1.7.0]: https://github.com/nardew/talipp/compare/1.6.0...1.7.0
[1.6.0]: https://github.com/nardew/talipp/compare/1.5.0...1.6.0
[1.5.0]: https://github.com/nardew/talipp/compare/1.4.0...1.5.0
[1.4.0]: https://github.com/nardew/talipp/compare/1.3.0...1.4.0
[1.3.0]: https://github.com/nardew/talipp/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/nardew/talipp/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/nardew/talipp/compare/1.0.0...1.1.0
