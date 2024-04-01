import unittest

from talipp.indicators import VTX

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = VTX(14, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].plus_vtx, 1.133113, places = 5)
        self.assertAlmostEqual(ind[-3].minus_vtx, 0.818481, places = 5)

        self.assertAlmostEqual(ind[-2].plus_vtx, 1.141292, places = 5)
        self.assertAlmostEqual(ind[-2].minus_vtx, 0.834611, places = 5)

        self.assertAlmostEqual(ind[-1].plus_vtx, 1.030133, places = 5)
        self.assertAlmostEqual(ind[-1].minus_vtx, 0.968750, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(VTX(14, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(VTX(14, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(VTX(14, self.input_values))


if __name__ == '__main__':
    unittest.main()
