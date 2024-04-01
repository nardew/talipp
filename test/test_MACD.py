import unittest

from talipp.indicators import MACD

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = MACD(12, 26, 9, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].macd, 0.293541, places = 5)
        self.assertAlmostEqual(ind[-3].signal, 0.098639, places = 5)
        self.assertAlmostEqual(ind[-3].histogram, 0.194901, places = 5)

        self.assertAlmostEqual(ind[-2].macd, 0.326186, places = 5)
        self.assertAlmostEqual(ind[-2].signal, 0.144149, places = 5)
        self.assertAlmostEqual(ind[-2].histogram, 0.182037, places = 5)

        self.assertAlmostEqual(ind[-1].macd, 0.329698, places = 5)
        self.assertAlmostEqual(ind[-1].signal, 0.181259, places = 5)
        self.assertAlmostEqual(ind[-1].histogram, 0.148439, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(MACD(12, 26, 9, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(MACD(12, 26, 9, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(MACD(12, 26, 9, self.input_values))


if __name__ == '__main__':
    unittest.main()
