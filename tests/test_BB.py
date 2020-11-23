import unittest

from talipp.indicators import BB

from TalippTest import TalippTest


class TestBB(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = BB(5, 2, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].lb, 8.186646, places = 5)
        self.assertAlmostEqual(ind[-3].cb, 9.748000, places = 5)
        self.assertAlmostEqual(ind[-3].ub, 11.309353, places = 5)

        self.assertAlmostEqual(ind[-2].lb, 9.161539, places = 5)
        self.assertAlmostEqual(ind[-2].cb, 10.096000, places = 5)
        self.assertAlmostEqual(ind[-2].ub, 11.030460, places = 5)

        self.assertAlmostEqual(ind[-1].lb, 9.863185, places = 5)
        self.assertAlmostEqual(ind[-1].cb, 10.254000, places = 5)
        self.assertAlmostEqual(ind[-1].ub, 10.644814, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(BB(5, 2, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(BB(5, 2, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(BB(5, 2, self.input_values))


if __name__ == '__main__':
    unittest.main()
