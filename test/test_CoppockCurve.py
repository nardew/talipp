import unittest

from talipp.indicators import CoppockCurve

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = CoppockCurve(11, 14, 10, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 27.309482, places = 5)
        self.assertAlmostEqual(ind[-2], 26.109333, places = 5)
        self.assertAlmostEqual(ind[-1], 22.941006, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(CoppockCurve(11, 14, 10, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(CoppockCurve(11, 14, 10, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(CoppockCurve(11, 14, 10, self.input_values))


if __name__ == '__main__':
    unittest.main()
