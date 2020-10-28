import unittest

from talipp.indicators import ROC

from talippTest import ITAITest


class TestEMA(ITAITest):
    def setUp(self) -> None:
        self.input_values = list(ITAITest.CLOSE_TMPL)

    def test_init(self):
        ind = ROC(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 30.740740, places = 5)
        self.assertAlmostEqual(ind[-2], 26.608910, places = 5)
        self.assertAlmostEqual(ind[-1], 33.511348, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ROC(3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ROC(3, self.input_values))


if __name__ == '__main__':
    unittest.main()
