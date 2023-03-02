import numpy as np
from talipp.ohlcv import OHLCVFactory, OHLCV
from talipp.indicators import AccuDist, ADX, ALMA, AO, Aroon, ATR, BB, BOP, CCI, ChaikinOsc, ChandeKrollStop, CHOP, \
    CoppockCurve, DEMA, DonchianChannels, DPO, EMA, ForceIndex, HMA, Ichimoku, KAMA, KeltnerChannels, KST, KVO, \
    MACD, MassIndex, MeanDev, OBV, ROC, RSI, ParabolicSAR, SFX, SMA, SMMA, SOBV, StdDev, Stoch, StochRSI, \
    SuperTrend, TEMA, TRIX, TSI, TTM, UO, VTX, VWAP, VWMA, WMA, McGinleyDynamic


class IndicatorManager:
    def __init__(self, ohlcv: np.ndarray, max_len: int = 300):
        """
        :param ohlcv: (N, 5) numpy array, ordered by time (small to large)
                    open, high, low, close, volume
        """
        self.max_len = max_len

        close = list(ohlcv[:, 3])
        dollar_volume = list(ohlcv[:, 4] * ohlcv[:, 3])
        ohlcv = OHLCVFactory.from_matrix(ohlcv)

        self.indicators = {}
        self.indicators['AccuDist'] = AccuDist(ohlcv)
        self.indicators['ADX'] = ADX(14, 14, ohlcv)
        self.indicators['ALMA'] = ALMA(9, 0.85, 6.0, close)
        self.indicators['AO'] = AO(5, 34, ohlcv)
        self.indicators['Aroon'] = Aroon(14, ohlcv)
        self.indicators['ATR'] = ATR(14, ohlcv)
        self.indicators['BB'] = BB(5, 2.0, close)
        self.indicators['BOP'] = BOP(ohlcv)
        self.indicators['CCI'] = CCI(20, ohlcv)
        self.indicators['ChaikinOsc'] = ChaikinOsc(3, 10, ohlcv)
        self.indicators['ChandeKrollStop'] = ChandeKrollStop(10, 1.0, 9, ohlcv)
        self.indicators['CHOP'] = CHOP(14, ohlcv)
        self.indicators['CoppockCurve'] = CoppockCurve(11, 14, 10, close)
        self.indicators['DEMA'] = DEMA(20, close)
        self.indicators['DonchianChannels'] = DonchianChannels(20, ohlcv)
        self.indicators['DPO'] = DPO(20, close)
        self.indicators['EMA_7'] = EMA(7, close)
        self.indicators['EMA_25'] = EMA(25, close)
        self.indicators['EMA_99'] = EMA(99, close)
        self.indicators['ForceIndex'] = ForceIndex(13, ohlcv)
        self.indicators['HMA'] = HMA(14, close)
        self.indicators['Ichimoku'] = Ichimoku(26, 9, 52, 52, 26, ohlcv)
        self.indicators['KAMA'] = KAMA(10, 2, 30, close)
        self.indicators['KeltnerChannels'] = KeltnerChannels(20, 10, 2.0, 2.0, ohlcv)
        self.indicators['KST'] = KST(10, 10, 15, 10, 20, 10, 30, 15, 9, close)
        self.indicators['KVO'] = KVO(34, 55, ohlcv)
        self.indicators['MACD'] = MACD(12, 26, 9, close)
        self.indicators['MassIndex'] = MassIndex(9, 9, 10, ohlcv)
        self.indicators['McGinleyDynamic'] = McGinleyDynamic(14, close)
        self.indicators['MeanDev'] = MeanDev(20, close)
        self.indicators['OBV'] = OBV(ohlcv)
        self.indicators['ParabolicSAR'] = ParabolicSAR(0.02, 0.02, 0.2, ohlcv)
        self.indicators['ROC'] = ROC(10, close)
        self.indicators['RSI'] = RSI(14, close)
        self.indicators['SFX'] = SFX(12, 12, 3, ohlcv)
        self.indicators['SMA_7'] = SMA(7, close)
        self.indicators['SMA_25'] = SMA(25, close)
        self.indicators['SMA_99'] = SMA(99, close)
        self.indicators['SMAV_7'] = SMA(7, dollar_volume)  # special
        self.indicators['SMAV_25'] = SMA(25, dollar_volume)  # special
        self.indicators['SMAV_99'] = SMA(99, dollar_volume)  # special
        self.indicators['SMMA'] = SMMA(9, close)
        self.indicators['SOBV'] = SOBV(9, ohlcv)
        self.indicators['StdDev'] = StdDev(9, close)
        self.indicators['Stoch'] = Stoch(14, 3, ohlcv)
        self.indicators['StochRSI'] = StochRSI(14, 14, 3, 3, close)
        self.indicators['SuperTrend'] = SuperTrend(10, 3, ohlcv)
        self.indicators['TEMA'] = TEMA(25, close)
        self.indicators['TRIX'] = TRIX(18, close)
        self.indicators['TSI'] = TSI(13, 25, close)
        self.indicators['TTM'] = TTM(20, 2, 1.5, ohlcv)
        self.indicators['UO'] = UO(7, 14, 28, ohlcv)
        self.indicators['VTX'] = VTX(14, ohlcv)
        self.indicators['VWAP'] = VWAP(ohlcv)
        self.indicators['VWMA'] = VWMA(25, ohlcv)
        self.indicators['WMA'] = WMA(10, close)

    def update_indicators(self, open: float, high: float, low: float, close: float, volume: float):
        for key in self.indicators:
            if isinstance(self.indicators[key].input_values[-1], float):
                if 'SMAV' in key:
                    self.indicators[key].add_input_value(close * volume)
                else:
                    self.indicators[key].add_input_value(close)
            else:
                ohlcv = OHLCV(open=open, high=high, low=low, close=close, volume=volume)
                self.indicators[key].add_input_value(ohlcv)
            while len(self.indicators[key]) > self.max_len:
                self.indicators[key].purge_oldest(1)

    def get_latest_indicators(self) -> dict:
        latest_indicators = {}
        for key in self.indicators:
            if isinstance(self.indicators[key][-1], float):
                latest_indicators[key] = self.indicators[key][-1]
            else:
                key_value_pairs = self.indicators[key].to_lists()
                for key2 in key_value_pairs:
                    value = key_value_pairs[key2][-1]
                    if not isinstance(value, float):
                        if key == 'ParabolicSAR' or key == 'SuperTrend':
                            value = value.value - 1
                    latest_indicators[f"{key}_{key2}"] = value
        return latest_indicators
