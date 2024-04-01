import unittest

from talipp.exceptions import TalippException
from talipp.indicator_util import composite_to_lists, has_valid_values, previous_if_exists
from talipp.indicators import BB, SMA


class Test(unittest.TestCase):
    def test_to_list(self):
        bb = BB(3, 2, [1, 2, 3, 4, 5])
        bb_lists = composite_to_lists(bb)

        print(bb_lists)

        self.assertTrue('lb' in bb_lists)
        self.assertTrue('cb' in bb_lists)
        self.assertTrue('ub' in bb_lists)

        self.assertEqual(len(bb_lists['lb']), 5)
        self.assertEqual(len(bb_lists['cb']), 5)
        self.assertEqual(len(bb_lists['ub']), 5)

        self.assertListEqual(bb_lists['cb'], [None, None, 2.0, 3.0, 4.0])

    def test_to_list_simple_type(self):
        sma = SMA(3, [1, 2, 3, 4, 5])

        with self.assertRaises(TalippException) as e:
            composite_to_lists(sma)

        print(e.exception)
        self.assertTrue('composite_to_lists(...) method can be used only with indicators returning composite output values, '
                        'this indicator returns' in e.exception.args[0])

    def test_to_list_empty(self):
        bb = BB(3, 2)
        bb_lists = composite_to_lists(bb)

        print(bb_lists)

        self.assertDictEqual(bb_lists, {})

    def test_has_valid_values(self):
        self.assertTrue(has_valid_values([1], 1))
        self.assertTrue(has_valid_values([1, 2], 1))

        self.assertTrue(has_valid_values([1], 1, exact=True))
        self.assertFalse(has_valid_values([1, 2], 1, exact=True))
        self.assertFalse(has_valid_values([], 1, exact=True))
        self.assertFalse(has_valid_values([None], 1, exact=True))
        self.assertFalse(has_valid_values([1, None], 1, exact=True))

        self.assertFalse(has_valid_values([], 1))
        self.assertFalse(has_valid_values([None], 1))
        self.assertFalse(has_valid_values([1, None], 1))

    def test_previous_if_exists(self):
        self.assertEqual(previous_if_exists([]), 0)
        self.assertEqual(previous_if_exists([], default=1), 1)
        self.assertEqual(previous_if_exists([1]), 1)
        self.assertEqual(previous_if_exists([1], index=-2), 0)
        self.assertEqual(previous_if_exists([1,2], index=-2), 1)


if __name__ == '__main__':
    unittest.main()
