import unittest

from talipp.indicators import MassIndex

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = MassIndex(9, 9, 10, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.498975, places = 5)
        self.assertAlmostEqual(ind[-2], 9.537927, places = 5)
        self.assertAlmostEqual(ind[-1], 9.648128, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(MassIndex(9, 9, 10, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(MassIndex(9, 9, 10, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(MassIndex(9, 9, 10, self.input_values))


if __name__ == '__main__':
    unittest.main()
