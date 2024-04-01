import unittest

from talipp.indicators import StochRSI

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = StochRSI(14, 14, 3, 3, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].k, 100.000000, places = 5)
        self.assertAlmostEqual(ind[-3].d, 82.573394, places = 5)

        self.assertAlmostEqual(ind[-2].k, 92.453271, places = 5)
        self.assertAlmostEqual(ind[-2].d, 92.500513, places = 5)

        self.assertAlmostEqual(ind[-1].k, 80.286409, places = 5)
        self.assertAlmostEqual(ind[-1].d, 90.913227, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(StochRSI(14, 14, 3, 3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(StochRSI(14, 14, 3, 3, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(StochRSI(14, 14, 3, 3, self.input_values))


if __name__ == '__main__':
    unittest.main()
