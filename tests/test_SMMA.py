import unittest

from talipp.indicators import SMMA

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = SMMA(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.149589, places = 5)
        self.assertAlmostEqual(ind[-2], 9.203610, places = 5)
        self.assertAlmostEqual(ind[-1], 9.243429, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(SMMA(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(SMMA(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(SMMA(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
