import unittest

from TalippTest import TalippTest
from talipp.indicators import SMA


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = SMA(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.075500, places = 5)
        self.assertAlmostEqual(ind[-2], 9.183000, places = 5)
        self.assertAlmostEqual(ind[-1], 9.308500, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(SMA(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(SMA(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(SMA(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
