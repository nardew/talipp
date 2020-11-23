import unittest

from talipp.indicators import KVO

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = KVO(5, 10, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 4540.325257, places = 5)
        self.assertAlmostEqual(ind[-2], 535.632479, places = 5)
        self.assertAlmostEqual(ind[-1], -2470.776132, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(KVO(5, 10, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(KVO(5, 10, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(KVO(5, 10, self.input_values))


if __name__ == '__main__':
    unittest.main()
