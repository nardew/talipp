import unittest

from talipp.indicators import NATR

from TalippTest import TalippTest


class TestATR(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = NATR(5, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 6.387410, places = 5)
        self.assertAlmostEqual(ind[-2], 6.501871, places = 5)
        self.assertAlmostEqual(ind[-1], 6.861131, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(NATR(5, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(NATR(5, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(NATR(5, self.input_values))


if __name__ == '__main__':
    unittest.main()
