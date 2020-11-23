import unittest

from talipp.indicators import Aroon

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = Aroon(10, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].up, 100, places = 5)
        self.assertAlmostEqual(ind[-3].down, 70, places = 5)

        self.assertAlmostEqual(ind[-2].up, 90, places = 5)
        self.assertAlmostEqual(ind[-2].down, 60, places = 5)

        self.assertAlmostEqual(ind[-1].up, 80, places = 5)
        self.assertAlmostEqual(ind[-1].down, 50, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(Aroon(10, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(Aroon(10, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(Aroon(10, self.input_values))


if __name__ == '__main__':
    unittest.main()
