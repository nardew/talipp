import unittest

from talipp.indicators import ChandeKrollStop

from TalippTest import TalippTest


class TestBB(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = ChandeKrollStop(5, 2, 3, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].short_stop, 9.507146, places = 5)
        self.assertAlmostEqual(ind[-3].long_stop, 9.772853, places = 5)

        self.assertAlmostEqual(ind[-2].short_stop, 9.529717, places = 5)
        self.assertAlmostEqual(ind[-2].long_stop, 9.750282, places = 5)

        self.assertAlmostEqual(ind[-1].short_stop, 9.529717, places = 5)
        self.assertAlmostEqual(ind[-1].long_stop, 9.750282, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ChandeKrollStop(5, 2, 3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ChandeKrollStop(5, 2, 3, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ChandeKrollStop(5, 2, 3, self.input_values))


if __name__ == '__main__':
    unittest.main()
