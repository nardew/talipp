import unittest

from talipp.indicators import KST

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = KST(5, 5, 10, 5, 15, 5, 25, 10, 9, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].kst, 136.602283, places = 5)
        self.assertAlmostEqual(ind[-3].signal, 103.707431, places = 5)

        self.assertAlmostEqual(ind[-2].kst, 158.252762, places = 5)
        self.assertAlmostEqual(ind[-2].signal, 113.964023, places = 5)

        self.assertAlmostEqual(ind[-1].kst, 155.407034, places = 5)
        self.assertAlmostEqual(ind[-1].signal, 122.246497, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(KST(10, 10, 15, 10, 20, 10, 30, 15, 9, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(KST(10, 10, 15, 10, 20, 10, 30, 15, 9, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(KST(10, 10, 15, 10, 20, 10, 30, 15, 9, self.input_values))


if __name__ == '__main__':
    unittest.main()
