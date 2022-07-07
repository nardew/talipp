import unittest

from talipp.indicators import TTM

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = TTM(20, 2, 2, input_values = self.input_values)

        print(ind)

        self.assertTrue(ind[-12].squeeze)
        self.assertAlmostEqual(ind[-12].histogram, 0.778771, places = 5)

        self.assertFalse(ind[-3].squeeze)
        self.assertAlmostEqual(ind[-3].histogram, 1.135782, places = 5)

        self.assertFalse(ind[-2].squeeze)
        self.assertAlmostEqual(ind[-2].histogram, 1.136939, places = 5)

        self.assertFalse(ind[-1].squeeze)
        self.assertAlmostEqual(ind[-1].histogram, 1.036864, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(TTM(20, 2, 2, input_values = self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(TTM(20, 2, 2, input_values = self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(TTM(20, 2, 2, input_values = self.input_values))


if __name__ == '__main__':
    unittest.main()
