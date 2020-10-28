import unittest

from talipp.indicators import OBV

from talippTest import ITAITest


class Test(ITAITest):
    def setUp(self) -> None:
        self.input_values = list(ITAITest.OHLCV_TMPL)

    def test_init(self):
        ind = OBV(self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 665.899999, places = 5)
        self.assertAlmostEqual(ind[-2], 617.609999, places = 5)
        self.assertAlmostEqual(ind[-1], 535.949999, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(OBV(self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(OBV(self.input_values))


if __name__ == '__main__':
    unittest.main()
