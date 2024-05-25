import unittest

from TalippTest import TalippTest
from talipp.exceptions import TalippException
from talipp.indicators import ZigZag
from talipp.indicators.ZigZag import PivotType
from talipp.ohlcv import OHLCV


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = ZigZag(0.05, 3, self.input_values)

        print(ind)

        self.assertEqual(ind[-3].type, PivotType.HIGH)
        self.assertEqual(ind[-3].ohlcv, OHLCV(open=9.16, high=10.1, low=9.16, close=9.76, volume=199.2, time=None))

        self.assertEqual(ind[-2].type, PivotType.LOW)
        self.assertEqual(ind[-2].ohlcv, OHLCV(open=9.18, high=9.32, low=8.6, close=9.32, volume=29.73, time=None))

        self.assertEqual(ind[-1].type, PivotType.HIGH)
        self.assertEqual(ind[-1].ohlcv, OHLCV(open=10.29, high=10.86, low=10.19, close=10.59, volume=108.27, time=None))

    def test_update(self):
        zigzag = ZigZag(0.5, 5, self.input_values)

        with self.assertRaises(TalippException) as e:
            zigzag.update(1)

        print(e.exception)
        self.assertTrue(
            'Operation not supported.' in e.exception.args[0])

    def test_delete(self):
        zigzag = ZigZag(0.5, 5, self.input_values)

        with self.assertRaises(TalippException) as e:
            zigzag.remove()

        print(e.exception)
        self.assertTrue(
            'Operation not supported.' in e.exception.args[0])

    def test_purge_oldest(self):
        zigzag = ZigZag(0.5, 5, self.input_values)

        with self.assertRaises(TalippException) as e:
            zigzag.purge_oldest(1)

        print(e.exception)
        self.assertTrue(
            'Operation not supported.' in e.exception.args[0])


if __name__ == '__main__':
    unittest.main()
