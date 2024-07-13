import unittest

from talipp.indicators import IR, RIR

from TalippTest import TalippTest


class TestIR(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = IR(self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.670000, places = 5)
        self.assertAlmostEqual(ind[-2], 0.620000, places = 5)
        self.assertAlmostEqual(ind[-1], 0.770000, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(IR(self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(IR(self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(IR(self.input_values))


class TestRIR(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = RIR(self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.065111, places = 5)
        self.assertAlmostEqual(ind[-2], 0.057567, places = 5)
        self.assertAlmostEqual(ind[-1], 0.074903, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(RIR(self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(RIR(self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(RIR(self.input_values))


if __name__ == '__main__':
    unittest.main()
