import os
import datetime

from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair
from cryptoxlib.clients.bitpanda import enums
from cryptoxlib.version_conversions import async_run

from talipp.ohlcv import OHLCV
from talipp.indicators import AccuDist, ADX, ALMA, AO, Aroon, ATR, BB, BOP, ChaikinOsc, CoppockCurve, DEMA, DonchianChannels, EMA, HMA, Ichimoku, \
    KAMA, KeltnerChannels, KST, MACD, MassIndex, OBV, PivotsHL, ROC, RSI, ParabolicSAR, SFX, SMA, SMMA, SOBV, StdDev, \
    Stoch, StochRSI, TEMA, TRIX, TSI, UO, VWMA, WMA


async def run():
    api_key = os.environ['BITPANDAAPIKEY']

    client = CryptoXLib.create_bitpanda_client(api_key)

    candles = await client.get_candlesticks(Pair('BTC', 'EUR'), enums.TimeUnit.DAYS, "1",
                                  datetime.datetime.now() - datetime.timedelta(days = 1500), datetime.datetime.now())
    candles = candles['response']
    close = [float(x['close']) for x in candles]
    ohlcv = [OHLCV(float(x['open']), float(x['high']), float(x['low']), float(x['close']), float(x['volume'])) for x in candles]
    print(f"Last OHLCV: {ohlcv[-1]}")

    print(f'AccuDist: {AccuDist(ohlcv)[-1]}')
    print(f'ADX: {ADX(14, 14, ohlcv)[-1]}')
    print(f'ALMA: {ALMA(9, 0.85, 6, close)[-1]}')
    print(f'AO: {AO(5, 34, ohlcv)[-1]}')
    print(f'Aroon: {Aroon(4, ohlcv)[-1]}')
    print(f'ATR: {ATR(14, ohlcv)[-1]}')
    print(f'BB: {BB(20, 2, close)[-1]}')
    print(f'BOP: {BOP(ohlcv)[-1]}')
    print(f'ChaikinOsc: {ChaikinOsc(3, 10, ohlcv)[-1]}')
    print(f'CoppockCurve: {CoppockCurve(11, 14, 10, close)[-1]}')
    print(f'DEMA: {DEMA(20, close)[-1]}')
    print(f'DonchianChannels: {DonchianChannels(20, ohlcv)[-1]}')
    print(f'EMA: {EMA(20, close)[-1]}')
    print(f'HMA: {HMA(9, close)[-1]}')
    print(f'Ichimoku: {Ichimoku(26, 9, 52, 52, 26, ohlcv)[-1]}')
    print(f'KAMA: {KAMA(14, 2, 30, close)[-1]}')
    print(f'KeltnerChannels: {KeltnerChannels(20, 26, 1, 1, ohlcv)[-1]}')
    print(f'KST: {KST(10, 10, 15, 10, 20, 10, 30, 15, 9, close)[-1]}')
    print(f'MACD: {MACD(12, 26, 9, close)[-1]}')
    print(f'MassIndex: {MassIndex(9, 9, 10, ohlcv)[-1]}')
    print(f'OBV: {OBV(ohlcv)[-1]}')
    print(f'Pivots: {PivotsHL(15, 15, ohlcv)[-4:]}')
    print(f'ROC: {ROC(9, close)[-1]}')
    print(f'RSI: {RSI(14, close)[-1]}')
    print(f"SAR: {ParabolicSAR(0.02, 0.02, 0.2, ohlcv)[-20:]}")
    print(f'SFX: {SFX(12, 12, 3, ohlcv)[-1]}')
    print(f'SMA: {SMA(20, close)[-1]}')
    print(f'SMMA: {SMMA(7, close)[-1]}')
    print(f'SOBV: {SOBV(7, ohlcv)[-1]}')
    print(f'StdDev: {StdDev(7, close)[-1]}')
    print(f'Stoch: {Stoch(14, 3, ohlcv)[-1]}')
    print(f'StochRSI: {StochRSI(14, 14, 3, 3, close)[-1]}')
    print(f'TEMA: {TEMA(20, close)[-1]}')
    print(f'TRIX: {TRIX(18, close)[-1]}')
    print(f'TSI: {TSI(13, 25, close)[-1]}')
    print(f'UO: {UO(7, 14, 28, ohlcv)[-1]}')
    print(f'VWMA: {VWMA(20, ohlcv)[-1]}')
    print(f'WMA: {WMA(9, close)[-1]}')

    await client.close()

if __name__ == "__main__":
    async_run(run())
