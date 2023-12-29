import unittest

from TalippTest import TalippTest
from talipp.indicators import T3


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = T3(5, 0.7, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.718661, places = 5)
        self.assertAlmostEqual(ind[-2], 9.968503, places = 5)
        self.assertAlmostEqual(ind[-1], 10.124616, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(T3(5, 0.7, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(T3(5, 0.7, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(T3(5, 0.7, self.input_values))


if __name__ == '__main__':
    unittest.main()
