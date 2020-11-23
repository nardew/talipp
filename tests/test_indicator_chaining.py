import unittest

from talipp.indicators import SMA

from TalippTest import TalippTest


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

        self.assertAlmostEqual(sma4[-2], 5)
        self.assertAlmostEqual(sma4[-1], 6)

    def test_iterative_add(self):
        sma1 = SMA(3)
        sma2 = SMA(3, input_indicator = sma1)
        sma3 = SMA(3, input_indicator = sma2)
        sma4 = SMA(3, input_indicator = sma3)

        for i in range(1, 11):
            sma1.add_input_value(i)

        print(sma1)
        print(sma2)
        print(sma3)
        print(sma4)

        self.assertAlmostEqual(sma4[-2], 5)
        self.assertAlmostEqual(sma4[-1], 6)

    def test_update(self):
        sma1 = SMA(3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        sma2 = SMA(3, input_indicator = sma1)
        sma3 = SMA(3, input_indicator = sma2)
        sma4 = SMA(3, input_indicator = sma3)

        last_indicator_value = sma4[-1]
        last_input_value = sma1.input_values[-1]

        for i in range(1, 20):
            sma1.update_input_value(i)

        sma1.update_input_value(last_input_value)

        self.assertEqual(last_indicator_value, sma4[-1])

    def test_delete(self):
        sma1 = SMA(3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        sma2 = SMA(3, input_indicator = sma1)
        sma3 = SMA(3, input_indicator = sma2)
        sma4 = SMA(3, input_indicator = sma3)

        last_indicator_value = sma4[-1]

        for i in range(1, 20):
            sma1.add_input_value(i)

        for i in range(1, 20):
            sma1.remove_input_value()

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


if __name__ == '__main__':
    unittest.main()
