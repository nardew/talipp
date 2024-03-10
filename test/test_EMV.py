import unittest

from talipp.indicators import EMV

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = EMV(14, 10000, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 5.656780, places = 5)
        self.assertAlmostEqual(ind[-2], 5.129971, places = 5)
        self.assertAlmostEqual(ind[-1], -0.192883, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(EMV(14, 10000, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(EMV(14, 10000, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(EMV(14, 10000, self.input_values))


if __name__ == '__main__':
    unittest.main()
