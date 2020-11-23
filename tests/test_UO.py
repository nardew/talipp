import unittest

from talipp.indicators import UO

from TalippTest import TalippTest


class TestAO(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = UO(3, 5, 7, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 67.574669, places = 5)
        self.assertAlmostEqual(ind[-2], 54.423675, places = 5)
        self.assertAlmostEqual(ind[-1], 47.901125, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(UO(3, 5, 7, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(UO(3, 5, 7, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(UO(3, 5, 7, self.input_values))


if __name__ == '__main__':
    unittest.main()
