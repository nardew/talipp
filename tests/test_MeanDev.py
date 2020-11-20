import unittest

from talipp.indicators import MeanDev

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = MeanDev(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.608949, places = 5)
        self.assertAlmostEqual(ind[-2], 0.595400, places = 5)
        self.assertAlmostEqual(ind[-1], 0.535500, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(MeanDev(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(MeanDev(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(MeanDev(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
