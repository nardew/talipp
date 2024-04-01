import unittest

from talipp.indicators import TSI

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)
        self.input_values_equal = list(TalippTest.CLOSE_EQUAL_VALUES_TMPL)

    def test_init(self):
        ind = TSI(14, 23, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.159520, places = 5)
        self.assertAlmostEqual(ind[-2], 10.724944, places = 5)
        self.assertAlmostEqual(ind[-1], 11.181863, places = 5)

    def test_init_equal(self):
        """ Check that if there is no price difference between two consecutive prices, the indicator does not crash"""
        ind = TSI(3, 5, self.input_values_equal)

        print(ind)

        self.assertSetEqual(set(ind), {None})

    def test_update(self):
        self.assertIndicatorUpdate(TSI(14, 23, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(TSI(14, 23, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(TSI(14, 23, self.input_values))


if __name__ == '__main__':
    unittest.main()
