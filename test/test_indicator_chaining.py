import unittest

from TalippTest import TalippTest
from talipp.indicators import SMA, MACD
from talipp.ohlcv import OHLCV


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        sma1 = SMA(3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        sma2 = SMA(3, input_indicator = sma1)
        sma3 = SMA(3, input_indicator = sma2)
        sma4 = SMA(3, input_indicator = sma3)

        print(sma1)
        print(sma2)
        print(sma3)
        print(sma4)

        self.assertListEqual(list(sma1), [None, None, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        self.assertListEqual(list(sma2), [None, None, None, None, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        self.assertListEqual(list(sma3), [None, None, None, None, None, None, 4.0, 5.0, 6.0, 7.0])
        self.assertListEqual(list(sma4), [None, None, None, None, None, None, None, None, 5.0, 6.0])

    def test_iterative_add(self):
        sma1 = SMA(3)
        sma2 = SMA(3, input_indicator = sma1)
        sma3 = SMA(3, input_indicator = sma2)
        sma4 = SMA(3, input_indicator = sma3)

        for i in range(1, 11):
            sma1.add(i)

        print(sma1)
        print(sma2)
        print(sma3)
        print(sma4)

        self.assertListEqual(list(sma1), [None, None, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        self.assertListEqual(list(sma2), [None, None, None, None, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        self.assertListEqual(list(sma3), [None, None, None, None, None, None, 4.0, 5.0, 6.0, 7.0])
        self.assertListEqual(list(sma4), [None, None, None, None, None, None, None, None, 5.0, 6.0])

    def test_update(self):
        sma1 = SMA(3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        sma2 = SMA(3, input_indicator = sma1)
        sma3 = SMA(3, input_indicator = sma2)
        sma4 = SMA(3, input_indicator = sma3)

        last_indicator_value = sma4[-1]
        last_input_value = sma1.input_values[-1]

        for i in range(1, 20):
            sma1.update(i)

        sma1.update(last_input_value)

        self.assertEqual(last_indicator_value, sma4[-1])

    def test_delete(self):
        sma1 = SMA(3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        sma2 = SMA(3, input_indicator = sma1)
        sma3 = SMA(3, input_indicator = sma2)
        sma4 = SMA(3, input_indicator = sma3)

        last_indicator_value = sma4[-1]

        for i in range(1, 20):
            sma1.add(i)

        for i in range(1, 20):
            sma1.remove()

        self.assertEqual(last_indicator_value, sma4[-1])

    def test_purge_oldest(self):
        sma1 = SMA(3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        sma2 = SMA(3, input_indicator = sma1)
        sma3 = SMA(3, input_indicator = sma2)
        sma4 = SMA(3, input_indicator = sma3)

        # purge oldest N values
        purge_size = 2
        sma1_copy = sma1[:]
        sma2_copy = sma2[:]
        sma3_copy = sma3[:]
        sma4_copy = sma4[:]
        sma1.purge_oldest(purge_size)
        self.assertSequenceEqual(sma1_copy[purge_size:], sma1)
        self.assertSequenceEqual(sma2_copy[purge_size:], sma2)
        self.assertSequenceEqual(sma3_copy[purge_size:], sma3)
        self.assertSequenceEqual(sma4_copy[purge_size:], sma4)

        # purge all remaining values
        purge_size = len(sma1)
        sma1_copy = sma1[:]
        sma2_copy = sma2[:]
        sma3_copy = sma3[:]
        sma4_copy = sma4[:]
        sma1.purge_oldest(purge_size)
        self.assertSequenceEqual(sma1_copy[purge_size:], sma1)
        self.assertSequenceEqual(sma2_copy[purge_size:], sma2)
        self.assertSequenceEqual(sma3_copy[purge_size:], sma3)
        self.assertSequenceEqual(sma4_copy[purge_size:], sma4)
        self.assertSequenceEqual([], sma1)
        self.assertSequenceEqual([], sma2)
        self.assertSequenceEqual([], sma3)
        self.assertSequenceEqual([], sma4)

    def test_composite_sub_indicator(self):
        ohlcv_input = list(TalippTest.OHLCV_TMPL)
        ind = MACD(12, 26, 9, ohlcv_input, input_modifier=lambda x: x.close)

        print(ind)

        self.assertAlmostEqual(ind[-3].macd, 0.293541, places=5)
        self.assertAlmostEqual(ind[-3].signal, 0.098639, places=5)
        self.assertAlmostEqual(ind[-3].histogram, 0.194901, places=5)

        self.assertAlmostEqual(ind[-2].macd, 0.326186, places=5)
        self.assertAlmostEqual(ind[-2].signal, 0.144149, places=5)
        self.assertAlmostEqual(ind[-2].histogram, 0.182037, places=5)

        self.assertAlmostEqual(ind[-1].macd, 0.329698, places=5)
        self.assertAlmostEqual(ind[-1].signal, 0.181259, places=5)
        self.assertAlmostEqual(ind[-1].histogram, 0.148439, places=5)


if __name__ == '__main__':
    unittest.main()
