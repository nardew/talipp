import unittest

from talipp.indicators import CCI

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = CCI(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 179.169127, places = 5)
        self.assertAlmostEqual(ind[-2], 141.667617, places = 5)
        self.assertAlmostEqual(ind[-1], 89.601438, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(CCI(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(CCI(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(CCI(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
