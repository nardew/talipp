import unittest

from talipp.indicators import HMA

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = HMA(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.718018, places = 5)
        self.assertAlmostEqual(ind[-2], 9.940188, places = 5)
        self.assertAlmostEqual(ind[-1], 10.104067, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(HMA(3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(HMA(3, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(HMA(3, self.input_values))


if __name__ == '__main__':
    unittest.main()
