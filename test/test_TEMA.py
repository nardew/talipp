import unittest

from talipp.indicators import TEMA

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = TEMA(10, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 10.330217, places = 5)
        self.assertAlmostEqual(ind[-2], 10.399910, places = 5)
        self.assertAlmostEqual(ind[-1], 10.323950, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(TEMA(10, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(TEMA(10, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(TEMA(10, self.input_values))


if __name__ == '__main__':
    unittest.main()
