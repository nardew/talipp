import unittest

from talipp.indicators import DPO

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = DPO(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.344499, places = 5)
        self.assertAlmostEqual(ind[-2], 0.116999, places = 5)
        self.assertAlmostEqual(ind[-1], 0.011499, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(DPO(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(DPO(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(DPO(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
