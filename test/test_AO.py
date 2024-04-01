import unittest

from talipp.indicators import AO

from TalippTest import TalippTest


class TestAO(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = AO(5, 7, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.117142, places = 5)
        self.assertAlmostEqual(ind[-2], 0.257142, places = 5)
        self.assertAlmostEqual(ind[-1], 0.373285, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(AO(5, 7, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(AO(5, 7, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(AO(5, 7, self.input_values))


if __name__ == '__main__':
    unittest.main()
