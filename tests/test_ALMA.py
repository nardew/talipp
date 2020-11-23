import unittest

from talipp.indicators import ALMA

from TalippTest import TalippTest


class TestALMA(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = ALMA(9, 0.85, 6, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.795859, places = 5)
        self.assertAlmostEqual(ind[-2], 10.121439, places = 5)
        self.assertAlmostEqual(ind[-1], 10.257038, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ALMA(9, 0.85, 6, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ALMA(9, 0.85, 6, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ALMA(9, 0.85, 6, self.input_values))


if __name__ == '__main__':
    unittest.main()
