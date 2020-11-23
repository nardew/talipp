import unittest

from talipp.indicators import StdDev

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = StdDev(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.800377, places = 5)
        self.assertAlmostEqual(ind[-2], 0.803828, places = 5)
        self.assertAlmostEqual(ind[-1], 0.721424, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(StdDev(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(StdDev(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(StdDev(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
