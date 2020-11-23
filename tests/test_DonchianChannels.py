import unittest

from talipp.indicators import DonchianChannels

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = DonchianChannels(5, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].lb, 8.420000, places = 5)
        self.assertAlmostEqual(ind[-3].cb, 9.640000, places = 5)
        self.assertAlmostEqual(ind[-3].ub, 10.860000, places = 5)

        self.assertAlmostEqual(ind[-2].lb, 8.420000, places = 5)
        self.assertAlmostEqual(ind[-2].cb, 9.640000, places = 5)
        self.assertAlmostEqual(ind[-2].ub, 10.860000, places = 5)

        self.assertAlmostEqual(ind[-1].lb, 9.260000, places = 5)
        self.assertAlmostEqual(ind[-1].cb, 10.059999, places = 5)
        self.assertAlmostEqual(ind[-1].ub, 10.860000, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(DonchianChannels(5, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(DonchianChannels(5, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(DonchianChannels(5, self.input_values))


if __name__ == '__main__':
    unittest.main()
