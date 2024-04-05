import unittest

from talipp.indicators import IBS

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = IBS(self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.597014, places = 5)
        self.assertAlmostEqual(ind[-2], 0.129032, places = 5)
        self.assertAlmostEqual(ind[-1], 0.493506, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(IBS(self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(IBS(self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(IBS(self.input_values))


if __name__ == '__main__':
    unittest.main()
