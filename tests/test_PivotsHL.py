import unittest

from talipp.indicators import PivotsHL
from talipp.indicators.PivotsHL import HLType

from TalippTest import TalippTest


class TestBB(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = PivotsHL(7, 7, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].ohlcv.open, 9.160000, places = 5)
        self.assertAlmostEqual(ind[-3].ohlcv.high, 10.10000, places = 5)
        self.assertAlmostEqual(ind[-3].ohlcv.low, 9.160000, places = 5)
        self.assertAlmostEqual(ind[-3].ohlcv.close, 9.760000, places = 5)
        self.assertAlmostEqual(ind[-3].ohlcv.volume, 199.200000, places = 5)
        self.assertAlmostEqual(ind[-3].type, HLType.HIGH, places = 5)

        self.assertAlmostEqual(ind[-2].ohlcv.open, 8.490000, places = 5)
        self.assertAlmostEqual(ind[-2].ohlcv.high, 9.400000, places = 5)
        self.assertAlmostEqual(ind[-2].ohlcv.low, 8.420000, places = 5)
        self.assertAlmostEqual(ind[-2].ohlcv.close, 9.210000, places = 5)
        self.assertAlmostEqual(ind[-2].ohlcv.volume, 120.020000, places = 5)
        self.assertAlmostEqual(ind[-2].type, HLType.LOW, places = 5)

        self.assertAlmostEqual(ind[-1].ohlcv.open, 10.290000, places = 5)
        self.assertAlmostEqual(ind[-1].ohlcv.high, 10.860000, places = 5)
        self.assertAlmostEqual(ind[-1].ohlcv.low, 10.190000, places = 5)
        self.assertAlmostEqual(ind[-1].ohlcv.close, 10.590000, places = 5)
        self.assertAlmostEqual(ind[-1].ohlcv.volume, 108.270000, places = 5)
        self.assertAlmostEqual(ind[-1].type, HLType.HIGH, places = 5)
    
    def test_update(self):
        self.assertIndicatorUpdate(PivotsHL(14, 14, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(PivotsHL(14, 14, self.input_values))

    # def test_purge_oldest(self):
    #     self.assertIndicatorPurgeOldest(PivotsHL(14, 14, self.input_values))

if __name__ == '__main__':
    unittest.main()
