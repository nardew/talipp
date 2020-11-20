import unittest

from talipp.indicators import ChaikinOsc

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = ChaikinOsc(5, 7, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 31.280810, places = 5)
        self.assertAlmostEqual(ind[-2], 28.688536, places = 5)
        self.assertAlmostEqual(ind[-1], 24.913310, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ChaikinOsc(5, 7, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ChaikinOsc(5, 7, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ChaikinOsc(5, 7, self.input_values))


if __name__ == '__main__':
    unittest.main()
