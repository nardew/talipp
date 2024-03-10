import unittest

from talipp.indicators import DEMA

from TalippTest import TalippTest


class TestDEMA(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = DEMA(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.683254, places = 5)
        self.assertAlmostEqual(ind[-2], 9.813792, places = 5)
        self.assertAlmostEqual(ind[-1], 9.882701, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(DEMA(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(DEMA(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(DEMA(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
