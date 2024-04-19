import unittest

from talipp.indicators import ALMA

from TalippTest import TalippTest


class TestALMA(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = ALMA(9, 0.85, 6, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 10.053326, places = 5)
        self.assertAlmostEqual(ind[-2], 10.267585, places = 5)
        self.assertAlmostEqual(ind[-1], 10.264363, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ALMA(9, 0.85, 6, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ALMA(9, 0.85, 6, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ALMA(9, 0.85, 6, self.input_values))


if __name__ == '__main__':
    unittest.main()
