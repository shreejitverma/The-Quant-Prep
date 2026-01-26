# coding: utf-8
#
# Simple Function
# (c) The Python Quants
#


def f(x):
    ''' Simple function to compute the square of a number.
    
    Parameters
    ==========
    x: float
        input number
    
    Returns
    =======
    y: float
        (positive) output number
        
    Raises
    ======
    ValueError if x is neither int or float
    '''
    if type(x) not in [int, float]:
        raise ValueError('Parameter must be integer or float.')
    y = x * x  # this line is changed
    return y
