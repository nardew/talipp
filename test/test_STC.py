import unittest

from talipp.indicators import STC

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = STC(5, 10, 10, 3, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 55.067364, places = 5)
        self.assertAlmostEqual(ind[-2], 82.248999, places = 5)
        self.assertAlmostEqual(ind[-1], 94.229147, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(STC(5, 10, 10, 3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(STC(5, 10, 10, 3, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(STC(5, 10, 10, 3, self.input_values))


if __name__ == '__main__':
    unittest.main()
