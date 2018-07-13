import unittest
import sys
from textwrap import dedent
import gje

    
class TestCase(unittest.TestCase):
    def assertRaisesRegex(self, *args, **kwargs):
        return (self.assertRaisesRegexp(*args, **kwargs)
            if sys.version_info[0] < 3
            else unittest.TestCase.assertRaisesRegex(self, *args, **kwargs))

def get_clause(m,lits):
    ## Deduce clause after GJE
    return gje.deduce_clause(m,lits)

def cols_state_to_matrix(state):
    ## Parse columns state to matrix
    return gje.columns_state_to_matrix(state)

def xor_columns(col,parity):
    ## XOR parity column with parity column
    return gje.xor_columns(col,parity)

def swap_row(m,i,j):
    ## Swap Rows m[i] with m[j]
    return gje.swap(m,i,j)
    
def xor_row(m,i,j):
    ## XOR Rows m[i] with m[j]
    return gje.xor(m,i,j)
    
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
    Parse the columns state to a binary matrix and return the list of literals
    """
    def test_column_state_to_matrix(self):
        self.assertEqual(cols_state_to_matrix(
        {'parity': [0, 1, 1, 0, 0], 2L: [1, 0, 0, 1, 0], 3L: [0, 0, 0, 0, 1], 4L: [1, 1, 0, 0, 0], 5L: [0, 1, 0, 0, 0], 6L: [1, 1, 0, 0, 0], 7L: [0, 0, 1, 0, 1], 8L: [0, 0, 1, 0, 0], 9L: [0, 0, 0, 1, 0], 10L: [0, 0, 0, 1, 0]}),
                         ([[1,0,1,0,1,0,0,0,0,0],
                           [0,0,1,1,1,0,0,0,0,1],
                           [0,0,0,0,0,1,1,0,0,1],
                           [1,0,0,0,0,0,0,1,1,0],
                           [0,1,0,0,0,1,0,0,0,0]],[2,3,4,5,6,7,8,9,10]))


    """
    Deduce clause after Gauss-Jordan Elimination
    """
    def test_imply_clause_one(self):
        self.assertEqual(get_clause([[1, 0, 0, 0],
                                     [0, 1, 1, 0],
                                     [0, 0, 0, 0]], [2,3,4]), [-2])

    def test_imply_clause_two(self):
        self.assertEqual(get_clause([[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 1]], [2,3,4]), [-2,-3,4])

    def test_imply_clause_three(self):
        self.assertEqual(get_clause([[1, 0, 1, 1, 0, 1],
                                     [0, 1, 1, 0, 0, 0],
                                     [1, 0, 1, 1, 1, 0]], [2,3,4,5,6]), [])

        
    """
    XOR a single column with Parity column Tests
    """
    def test_column_xor_one(self):
        self.assertEqual(xor_columns([1, 0],[1, 0]),[0, 0])

    def test_column_xor_two(self):
        self.assertEqual(xor_columns([0, 0, 0, 0, 0],[1, 1, 1, 1, 1]),[1, 1, 1, 1, 1])

    def test_column_xor_three(self):
        self.assertEqual(xor_columns([0, 1, 0, 1],[1, 0, 1, 0]),[1, 1, 1, 1])

    
        
    """
    Swap Rows Tests
    """
    def test_swap_one(self):
        self.assertEqual(swap_row([[1, 0, 1, 1, 1, 1],
                                   [1, 1, 0, 1, 0, 1],
                                   [1, 0, 0, 0, 0, 1]], 1, 2),[[1, 0, 1, 1, 1, 1],
                                                               [1, 0, 0, 0, 0, 1],
                                                               [1, 1, 0, 1, 0, 1]])

    def test_swap_two(self):
        self.assertEqual(swap_row([[0, 0],
                                   [1, 1]], 1, 0),[[1, 1],
                                                   [0, 0]])

    def test_swap_three(self):
        self.assertEqual(swap_row([[0, 1],
                                   [1, 0]], 1, 0),[[1, 0],
                                                   [0, 1]])

    """
    XOR Rows Tests
    """
    def test_xor_one(self):
        self.assertEqual(xor_row([[1, 0],
                                  [1, 1],
                                  [1, 0]], 0, 1),[[1, 0],
                                                  [0, 1],
                                                  [1, 0]])

    def test_xor_two(self):
        self.assertEqual(xor_row([[0, 0],
                                  [1, 1]], 1, 0),[[1, 1],
                                                  [1, 1]])

    def test_xor_three(self):
        self.assertEqual(xor_row([[0, 0],
                                  [0, 0]], 1, 0),[[0, 0],
                                                  [0, 0]])

        
    """
    Gauss-Jordan Elimination Tests

    The second parameter in the solve function is a flag.
    If True, it will display the GJ Elimination Procedure

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
