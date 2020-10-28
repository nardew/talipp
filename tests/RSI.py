import unittest

from talipp.indicators import RSI

from talippTest import ITAITest


class Test(ITAITest):
    def setUp(self) -> None:
        self.input_values = list(ITAITest.CLOSE_TMPL)

    def test_init(self):
        ind = RSI(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 57.880437, places = 5)
        self.assertAlmostEqual(ind[-2], 55.153392, places = 5)
        self.assertAlmostEqual(ind[-1], 53.459494, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(RSI(10, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(RSI(10, self.input_values))


if __name__ == '__main__':
    unittest.main()
