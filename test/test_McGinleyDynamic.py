import unittest

from talipp.indicators import McGinleyDynamic

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = McGinleyDynamic(14, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 8.839868, places = 5)
        self.assertAlmostEqual(ind[-2], 8.895229, places = 5)
        self.assertAlmostEqual(ind[-1], 8.944634, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(McGinleyDynamic(14, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(McGinleyDynamic(14, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(McGinleyDynamic(14, self.input_values))


if __name__ == '__main__':
    unittest.main()
