import unittest

from talipp.indicators import WMA

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = WMA(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.417523, places = 5)
        self.assertAlmostEqual(ind[-2], 9.527476, places = 5)
        self.assertAlmostEqual(ind[-1], 9.605285, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(WMA(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(WMA(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(WMA(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
