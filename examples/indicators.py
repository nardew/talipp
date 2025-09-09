import random

from talipp.indicators import AccuDist, ADX, ALMA, AO, Aroon, ATR, BB, BOP, CCI, ChaikinOsc, ChandeKrollStop, CHOP, \
    CoppockCurve, DEMA, DonchianChannels, DPO, EMA, EMV, ForceIndex, HMA, IBS, Ichimoku, KAMA, KeltnerChannels, KST, KVO, \
    MACD, MassIndex, MeanDev, NATR, OBV, ROC, RogersSatchell, RSI, ParabolicSAR, SFX, SMA, SMMA, SOBV, STC, StdDev, Stoch, StochRSI, \
    SuperTrend, T3, TEMA, TRIX, TSI, TTM, UO, VTX, VWAP, VWMA, Williams, WMA, ZigZag, ZLEMA
from talipp.ohlcv import OHLCVFactory

if __name__ == "__main__":

    close = random.sample(range(1, 10000), 1000)
    ohlcv = OHLCVFactory.from_matrix2([
        random.sample(range(1, 10000), 1000),
        random.sample(range(1, 10000), 1000),
        random.sample(range(1, 10000), 1000),
        random.sample(range(1, 10000), 1000),
        random.sample(range(1, 10000), 1000)]
    )
    print(f"Last OHLCV: {ohlcv[-1]}")

    print(f'AccuDist: {AccuDist(ohlcv)[-1]}')
    print(f'ADX: {ADX(14, 14, ohlcv)[-1]}')
    print(f'ALMA: {ALMA(9, 0.85, 6, close)[-1]}')
    print(f'AO: {AO(5, 34, ohlcv)[-1]}')
    print(f'Aroon: {Aroon(14, ohlcv)[-1]}')
    print(f'ATR: {ATR(14, ohlcv)[-1]}')
    print(f'BB: {BB(20, 2, close)[-1]}')
    print(f'BOP: {BOP(ohlcv)[-1]}')
    print(f'CCI: {CCI(20, ohlcv)[-1]}')
    print(f'ChaikinOsc: {ChaikinOsc(3, 10, ohlcv)[-1]}')
    print(f'ChandeKrollStop: {ChandeKrollStop(10, 2, 9, ohlcv)[-1]}')
    print(f'CHOP: {CHOP(14, ohlcv)[-1]}')
    print(f'CoppockCurve: {CoppockCurve(11, 14, 10, close)[-1]}')
    print(f'DEMA: {DEMA(20, close)[-1]}')
    print(f'DonchianChannels: {DonchianChannels(20, ohlcv)[-1]}')
    print(f'DPO: {DPO(20, close)[-1]}')
    print(f'EMA: {EMA(20, close)[-1]}')
    print(f'EMV: {EMV(14, 10000, ohlcv)[-1]}')
    print(f'ForceIndex: {ForceIndex(13, ohlcv)[-1]}')
    print(f'HMA: {HMA(9, close)[-1]}')
    print(f'IBS: {IBS(ohlcv)[-1]}')
    print(f'Ichimoku: {Ichimoku(26, 9, 52, 52, 26, ohlcv)[-1]}')
    print(f'KAMA: {KAMA(14, 2, 30, close)[-1]}')
    print(f'KeltnerChannels: {KeltnerChannels(20, 26, 1, 1, ohlcv)[-1]}')
    print(f'KST: {KST(10, 10, 15, 10, 20, 10, 30, 15, 9, close)[-1]}')
    print(f'KVO: {KVO(34, 55, ohlcv)[-1]}')
    print(f'MACD: {MACD(12, 26, 9, close)[-1]}')
    print(f'MassIndex: {MassIndex(9, 9, 10, ohlcv)[-1]}')
    print(f'MeanDev: {MeanDev(10, close)[-1]}')
    print(f'NATR: {NATR(14, ohlcv)[-1]}')
    print(f'OBV: {OBV(ohlcv)[-1]}')
    print(f'ROC: {ROC(9, close)[-1]}')
    print(f'RogersSatchell: {RogersSatchell(9, ohlcv)[-1]}')
    print(f'RSI: {RSI(14, close)[-1]}')
    print(f"SAR: {ParabolicSAR(0.02, 0.02, 0.2, ohlcv)[-20:]}")
    print(f'SFX: {SFX(12, 12, 3, ohlcv)[-1]}')
    print(f'SMA: {SMA(20, close)[-1]}')
    print(f'SMMA: {SMMA(7, close)[-1]}')
    print(f'SOBV: {SOBV(7, ohlcv)[-1]}')
    print(f'STC: {STC(23, 50, 10, 3, close)[-1]}')
    print(f'StdDev: {StdDev(7, close)[-1]}')
    print(f'Stoch: {Stoch(14, 3, ohlcv)[-1]}')
    print(f'StochRSI: {StochRSI(14, 14, 3, 3, close)[-1]}')
    print(f'SuperTrend: {SuperTrend(10, 3, ohlcv)[-20:]}')
    print(f'T3: {T3(20, 0.7, close)[-1]}')
    print(f'TEMA: {TEMA(20, close)[-1]}')
    print(f'TRIX: {TRIX(18, close)[-1]}')
    print(f'TSI: {TSI(13, 25, close)[-1]}')
    print(f'TTM: {TTM(20, input_values = ohlcv)[-20:]}')
    print(f'UO: {UO(7, 14, 28, ohlcv)[-1]}')
    print(f'VTX: {VTX(14, ohlcv)[-1]}')
    print(f'VWAP: {VWAP(ohlcv)[-1]}')
    print(f'VWMA: {VWMA(20, ohlcv)[-1]}')
    print(f'Williams: {Williams(9, ohlcv)[-1]}')
    print(f'WMA: {WMA(9, close)[-1]}')
    print(f'ZigZag: {ZigZag(0.1, 10, ohlcv)[-5:]}')
    print(f'ZLEMA: {ZLEMA(9, close)[-1]}')
