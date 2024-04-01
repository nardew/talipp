import unittest

from talipp.indicators import KeltnerChannels

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = KeltnerChannels(10, 10, 2, 3, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].lb, 7.606912, places = 5)
        self.assertAlmostEqual(ind[-3].cb, 9.643885, places = 5)
        self.assertAlmostEqual(ind[-3].ub, 11.001867, places = 5)

        self.assertAlmostEqual(ind[-2].lb, 7.731176, places = 5)
        self.assertAlmostEqual(ind[-2].cb, 9.750451, places = 5)
        self.assertAlmostEqual(ind[-2].ub, 11.096635, places = 5)

        self.assertAlmostEqual(ind[-1].lb, 7.747476, places = 5)
        self.assertAlmostEqual(ind[-1].cb, 9.795824, places = 5)
        self.assertAlmostEqual(ind[-1].ub, 11.161389, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(KeltnerChannels(10, 10, 2, 3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(KeltnerChannels(10, 10, 2, 3, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(KeltnerChannels(10, 10, 2, 3, self.input_values))


if __name__ == '__main__':
    unittest.main()
