import unittest

from talipp.indicators import TRIX

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = TRIX(10, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 66.062922, places = 5)
        self.assertAlmostEqual(ind[-2], 75.271366, places = 5)
        self.assertAlmostEqual(ind[-1], 80.317194, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(TRIX(10, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(TRIX(10, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(TRIX(10, self.input_values))


if __name__ == '__main__':
    unittest.main()
