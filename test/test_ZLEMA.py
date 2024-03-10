import unittest

from TalippTest import TalippTest
from talipp.indicators import ZLEMA


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = ZLEMA(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.738243, places = 5)
        self.assertAlmostEqual(ind[-2], 9.871744, places = 5)
        self.assertAlmostEqual(ind[-1], 9.975387, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ZLEMA(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ZLEMA(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ZLEMA(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
