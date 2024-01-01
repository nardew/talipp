import unittest

from talipp.indicators import SFX

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = SFX(12, 12, 3, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].atr, 0.689106, places = 5)
        self.assertAlmostEqual(ind[-3].std_dev, 0.572132, places = 5)
        self.assertAlmostEqual(ind[-3].ma_std_dev, 0.476715, places = 5)

        self.assertAlmostEqual(ind[-2].atr, 0.683347, places = 5)
        self.assertAlmostEqual(ind[-2].std_dev, 0.610239, places = 5)
        self.assertAlmostEqual(ind[-2].ma_std_dev, 0.551638, places = 5)

        self.assertAlmostEqual(ind[-1].atr, 0.690568, places = 5)
        self.assertAlmostEqual(ind[-1].std_dev, 0.619332, places = 5)
        self.assertAlmostEqual(ind[-1].ma_std_dev, 0.600567, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(SFX(12, 12, 3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(SFX(12, 12, 3, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(SFX(12, 12, 3, self.input_values))


if __name__ == '__main__':
    unittest.main()
