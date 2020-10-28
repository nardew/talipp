import unittest

from talipp.indicators import BB


class TestOHLC(unittest.TestCase):
    def test_conversion_to_list(self):
        bb = BB(3, 2, [1, 2, 3, 4, 5])
        bb_lists = bb.to_lists()
        print(bb_lists)

        self.assertTrue('lb' in bb_lists)
        self.assertTrue('cb' in bb_lists)
        self.assertTrue('ub' in bb_lists)

        self.assertEqual(len(bb_lists['lb']), 5)
        self.assertEqual(len(bb_lists['cb']), 5)
        self.assertEqual(len(bb_lists['ub']), 5)

        self.assertListEqual([bb_lists['lb'][0], bb_lists['lb'][1]], [None, None])
        self.assertListEqual([bb_lists['cb'][0], bb_lists['lb'][1]], [None, None])
        self.assertListEqual([bb_lists['ub'][0], bb_lists['lb'][1]], [None, None])

    def test_conversion_to_list_empty(self):
        bb = BB(3, 2)
        bb_lists = bb.to_lists()
        print(bb_lists)

        self.assertDictEqual(bb_lists, {})

if __name__ == '__main__':
    unittest.main()
