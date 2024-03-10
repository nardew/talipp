import unittest

from talipp.indicators import ADX

from TalippTest import TalippTest


class TestADX(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = ADX(14, 14, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].adx, 15.734865, places = 5)
        self.assertAlmostEqual(ind[-3].plus_di, 33.236743, places = 5)
        self.assertAlmostEqual(ind[-3].minus_di, 17.415377, places = 5)

        self.assertAlmostEqual(ind[-2].adx, 16.761395, places = 5)
        self.assertAlmostEqual(ind[-2].plus_di, 31.116720, places = 5)
        self.assertAlmostEqual(ind[-2].minus_di, 16.716048, places = 5)

        self.assertAlmostEqual(ind[-1].adx, 16.698475, places = 5)
        self.assertAlmostEqual(ind[-1].plus_di, 28.670782, places = 5)
        self.assertAlmostEqual(ind[-1].minus_di, 20.812570, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ADX(14, 14, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ADX(14, 14, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ADX(14, 14, self.input_values))


if __name__ == '__main__':
    unittest.main()
