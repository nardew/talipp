import unittest

from talipp.indicators import KAMA

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = KAMA(14, 2, 30, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 8.884374, places = 5)
        self.assertAlmostEqual(ind[-2], 8.932091, places = 5)
        self.assertAlmostEqual(ind[-1], 8.941810, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(KAMA(14, 2, 30, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(KAMA(14, 2, 30, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(KAMA(14, 2, 30, self.input_values))


if __name__ == '__main__':
    unittest.main()
