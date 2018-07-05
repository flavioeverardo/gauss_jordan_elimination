import unittest
import sys
from textwrap import dedent
import gje

    
class TestCase(unittest.TestCase):
    def assertRaisesRegex(self, *args, **kwargs):
        return (self.assertRaisesRegexp(*args, **kwargs)
            if sys.version_info[0] < 3
            else unittest.TestCase.assertRaisesRegex(self, *args, **kwargs))

def solve(m, show):
    matrix = []

    ## If there are more than unary xors perform GJE
    if len(m[0]) > 2:
        matrix = gje.remove_rows_zeros(m)
        matrix = gje.perform_gauss_jordan_elimination(matrix, show)
    
    return matrix


class TestProgramTransformer(TestCase):
    """
    The second parameter in the solve function is a flag.
    If True, it will display the GJ Elimination Procedure
    """

    ## More Columns
    def test_more_cols_one(self):
        self.assertEqual(solve([[0, 1, 1, 0, 0],
                                [0, 1, 1, 0, 0],
                                [1, 0, 0, 1, 0]],False),
                         [[1, 0, 0, 1, 0],
                          [0, 1, 1, 0, 0],
                          [0, 0, 0, 0, 0]])

    def test_more_cols_two(self):
        self.assertEqual(solve([[0, 1, 1, 0],
                                [0, 1, 1, 0],
                                [1, 0, 0, 0]],False),
                         [[1, 0, 0, 0],
                          [0, 1, 1, 0],
                          [0, 0, 0, 0]])

    def test_more_cols_three(self):
        self.assertEqual(solve([[1, 0, 1, 0, 0, 0, 0, 0],
                                [1, 1, 1, 0, 0, 0, 0, 1],
                                [0, 0, 0, 1, 1, 0, 0, 1],
                                [0, 0, 0, 0, 0, 1, 1, 0],
                                [0, 0, 0, 1, 0, 0, 0, 0]],False),
                         [[1, 0, 1, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 1],
                          [0, 0, 0, 0, 0, 1, 1, 0]])

    def test_more_cols_four(self):
        self.assertEqual(solve([[0, 1, 0, 0, 0, 0, 0, 1],
                                [0, 1, 1, 0, 0, 0, 0, 0],
                                [0, 0, 0, 1, 1, 0, 0, 1],
                                [0, 0, 0, 0, 0, 1, 1, 0],
                                [0, 1, 0, 0, 0, 0, 1, 0],
                                [1, 0, 0, 1, 0, 0, 0, 0]],False),
                         [[1, 0, 0, 0, 1, 0, 0, 1],
                          [0, 1, 0, 0, 0, 0, 0, 1],
                          [0, 0, 1, 0, 0, 0, 0, 1],
                          [0, 0, 0, 1, 1, 0, 0, 1],
                          [0, 0, 0, 0, 0, 1, 0, 1],
                          [0, 0, 0, 0, 0, 0, 1, 1]])

    def test_more_cols_five(self):
        self.assertEqual(solve([[1, 0, 1, 0, 1, 1, 0, 0],
                                [1, 1, 1, 0, 0, 0, 1, 1],
                                [0, 0, 1, 0, 1, 0, 0, 1],
                                [0, 1, 0, 1, 0, 1, 1, 0],
                                [0, 0, 0, 1, 0, 0, 0, 0]],False),
                         [[1, 0, 0, 0, 0, 1, 0, 1],
                          [0, 1, 0, 0, 0, 1, 1, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 1]])

    ## Square
    def test_square_one(self):
        self.assertEqual(solve([[1, 0, 1, 0, 1, 0],
                                [1, 1, 1, 0, 0, 1],
                                [0, 0, 1, 0, 1, 1],
                                [0, 1, 0, 1, 0, 0],
                                [0, 0, 0, 1, 0, 0]],False),
                         [[1, 0, 0, 0, 0, 1],
                          [0, 1, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 1, 1]])

    def test_square_two(self):
        self.assertEqual(solve([[1, 0, 1, 1, 1],
                                [1, 0, 1, 0, 0],
                                [0, 1, 0, 0, 1],
                                [0, 0, 1, 1, 0]],False),
                         [[1, 0, 0, 0, 1],
                          [0, 1, 0, 0, 1],
                          [0, 0, 1, 0, 1],
                          [0, 0, 0, 1, 1]])

    def test_square_three(self):
        self.assertEqual(solve([[1, 1, 1, 1],
                                [1, 0, 1, 0],
                                [0, 0, 1, 0]],False),
                         [[1, 0, 0, 0],
                          [0, 1, 0, 1],
                          [0, 0, 1, 0]])

    def test_square_four(self):
        self.assertEqual(solve([[0, 0, 1, 1, 1, 0],
                                [0, 1, 1, 1, 0, 1],
                                [1, 0, 1, 1, 1, 1],
                                [0, 1, 0, 1, 0, 0],
                                [1, 0, 0, 1, 0, 1]],False),
                         [[1, 0, 0, 0, 0, 1],
                          [0, 1, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 1],
                          [0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 1, 1]])

    def test_square_five(self):
        self.assertEqual(solve([[1, 1, 1],
                                [1, 0, 1]],False),
                         [[1, 0, 1],
                          [0, 1, 0]])


    ## More Rows
    def test_more_rows_one(self):
        self.assertEqual(solve([[1, 0, 1, 0],
                                [1, 1, 1, 0],
                                [0, 1, 0, 1],
                                [0, 0, 1, 0],
                                [0, 1, 0, 1]],False),
                         [[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1],
                          [0, 0, 0, 1]])

    def test_more_rows_two(self):
        self.assertEqual(solve([[0, 1, 0],
                                [0, 1, 1],
                                [1, 0, 0],
                                [1, 1, 0]],False),
                         [[1, 0, 0],
                          [0, 1, 1],
                          [0, 0, 1],
                          [0, 0, 1]])

    def test_more_rows_three(self):
        self.assertEqual(solve([[0, 1, 1],
                                [1, 0, 0],
                                [0, 0, 0]],False),
                         [[1, 0, 0],
                          [0, 1, 1]])
        
        

if __name__ == '__main__':
    unittest.main()        
