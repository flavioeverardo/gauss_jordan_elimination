import unittest
import sys
from textwrap import dedent
import gje

    
class TestCase(unittest.TestCase):
    def assertRaisesRegex(self, *args, **kwargs):
        return (self.assertRaisesRegexp(*args, **kwargs)
            if sys.version_info[0] < 3
            else unittest.TestCase.assertRaisesRegex(self, *args, **kwargs))

def check_sat(m):
    ## Check SAT
    return gje.check_sat(m)
    
def remove_rows_zeros(m):
    ## Remove rows with all zeros including the augmented column
    matrix = gje.remove_rows_zeros(m)
    return matrix
    
def solve_gje(m, show):
    ## If there are more than unary xors perform GJE
    if len(m[0]) > 2:
        m = gje.remove_rows_zeros(m)
        m = gje.perform_gauss_jordan_elimination(m, show)
    return m


class TestProgramTransformer(TestCase):
    """
    The second parameter in the solve function is a flag.
    If True, it will display the GJ Elimination Procedure
    """

    """ 
    Gauss-Jorda Elimination Tests
    """

    ## No GJE due matrix size. Return the same matrix to check SAT
    def test_no_gje_one(self):
        self.assertEqual(solve_gje([[1, 0],
                                    [1, 1],
                                    [1, 0]],False),
                         [[1, 0],
                          [1, 1],
                          [1, 0]])

    def test_no_gje_two(self):
        self.assertEqual(solve_gje([[1, 0],
                                    [0, 1]],False),
                         [[1, 0],
                          [0, 1]])
        
    
    ## More Columns than Rows
    def test_more_cols_one(self):
        self.assertEqual(solve_gje([[0, 1, 1, 0, 0],
                                    [0, 1, 1, 0, 0],
                                    [1, 0, 0, 1, 0]],False),
                         [[1, 0, 0, 1, 0],
                          [0, 1, 1, 0, 0],
                          [0, 0, 0, 0, 0]])

    def test_more_cols_two(self):
        self.assertEqual(solve_gje([[0, 1, 1, 0],
                                    [0, 1, 1, 0],
                                    [1, 0, 0, 0]],False),
                         [[1, 0, 0, 0],
                          [0, 1, 1, 0],
                          [0, 0, 0, 0]])

    def test_more_cols_three(self):
        self.assertEqual(solve_gje([[1, 0, 1, 0, 0, 0, 0, 0],
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
        self.assertEqual(solve_gje([[0, 1, 0, 0, 0, 0, 0, 1],
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
        self.assertEqual(solve_gje([[1, 0, 1, 0, 1, 1, 0, 0],
                                    [1, 1, 1, 0, 0, 0, 1, 1],
                                    [0, 0, 1, 0, 1, 0, 0, 1],
                                    [0, 1, 0, 1, 0, 1, 1, 0],
                                    [0, 0, 0, 1, 0, 0, 0, 0]],False),
                         [[1, 0, 0, 0, 0, 1, 0, 1],
                          [0, 1, 0, 0, 0, 1, 1, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 1]])

    ## Square Matrix
    def test_square_one(self):
        self.assertEqual(solve_gje([[1, 0, 1, 0, 1, 0],
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
        self.assertEqual(solve_gje([[1, 0, 1, 1, 1],
                                    [1, 0, 1, 0, 0],
                                    [0, 1, 0, 0, 1],
                                    [0, 0, 1, 1, 0]],False),
                         [[1, 0, 0, 0, 1],
                          [0, 1, 0, 0, 1],
                          [0, 0, 1, 0, 1],
                          [0, 0, 0, 1, 1]])

    def test_square_three(self):
        self.assertEqual(solve_gje([[1, 1, 1, 1],
                                    [1, 0, 1, 0],
                                    [0, 0, 1, 0]],False),
                         [[1, 0, 0, 0],
                          [0, 1, 0, 1],
                          [0, 0, 1, 0]])

    def test_square_four(self):
        self.assertEqual(solve_gje([[0, 0, 1, 1, 1, 0],
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
        self.assertEqual(solve_gje([[1, 1, 1],
                                    [1, 0, 1]],False),
                         [[1, 0, 1],
                          [0, 1, 0]])


    ## More Rows than Columns
    def test_more_rows_one(self):
        self.assertEqual(solve_gje([[1, 0, 1, 0],
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
        self.assertEqual(solve_gje([[0, 1, 0],
                                    [0, 1, 1],
                                    [1, 0, 0],
                                    [1, 1, 0]],False),
                         [[1, 0, 0],
                          [0, 1, 1],
                          [0, 0, 1],
                          [0, 0, 1]])

    def test_more_rows_three(self):
        self.assertEqual(solve_gje([[0, 1, 1],
                                    [1, 0, 0],
                                    [0, 0, 0]],False),
                         [[1, 0, 0],
                          [0, 1, 1]])


    """ 
    Pre GJE... Remove Rows if they are all zeros
    """
    ## Remove Rows full of Zeros 
    def test_remove_zeros_one(self):
        self.assertEqual(remove_rows_zeros([[1, 0, 1, 0],
                                            [1, 1, 1, 0],
                                            [0, 1, 0, 1],
                                            [0, 0, 0, 0],
                                            [0, 0, 0, 0]]),
                         [[1, 0, 1, 0],
                          [1, 1, 1, 0],
                          [0, 1, 0, 1]])

    def test_remove_zeros_two(self):
        self.assertEqual(remove_rows_zeros([[1, 0, 0],
                                            [0, 1, 1],
                                            [0, 0, 1],
                                            [0, 0, 0]]),
                         [[1, 0, 0],
                          [0, 1, 1],
                          [0, 0, 1]])

    def test_remove_zeros_three(self):
        self.assertEqual(remove_rows_zeros([[0, 1, 1],
                                            [1, 0, 0],
                                            [0, 0, 0]]),
                         [[0, 1, 1],
                          [1, 0, 0]])


    """ 
    Check Satisfiability wrt the augmented column. 
    It must exist an empty odd equation
    """
    ## Check SATISFIABILITY
    def test_check_sat_one(self):
        self.assertEqual(check_sat([[1, 0, 1, 0],
                                     [1, 1, 1, 0],
                                     [0, 1, 0, 1],
                                     [0, 0, 0, 1],
                                     [0, 0, 0, 0]]),True)

    def test_check_sat_two(self):
        self.assertEqual(check_sat([[1, 0, 0],
                                    [0, 1, 1],
                                    [1, 0, 1],
                                    [1, 1, 0]]),False)

    def test_check_sat_three(self):
        self.assertEqual(check_sat([[1, 0, 1],
                                    [0, 1, 0],
                                    [0, 0, 1]]),True)

    def test_check_sat_four(self):
        self.assertEqual(check_sat([[1, 0, 0, 0, 0, 0],
                                    [0, 1, 0, 0, 0, 1],
                                    [0, 0, 1, 0, 0, 1],
                                    [0, 0, 0, 1, 0, 0],
                                    [0, 0, 0, 0, 1, 1]]),False)
        

if __name__ == '__main__':
    unittest.main()        
