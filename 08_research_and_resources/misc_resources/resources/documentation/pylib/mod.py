#
# pylib Example
# mod.py
#
# The Python Quants GmbH
#
import doctest


def one(x):
    ''' Simple function.

    :Parameters:
        x: float
            input number

    :Returns:
        y: float
            output number

    :Raise:
        TypeError
            if x is not a number

    :Examples:
        >>> # from pylib import *
        >>> one(10)
        10
        >>> one(20)
        20
        >>> one('python')
        Traceback (most recent call last):
            ...
        TypeError: x must be of type int or float.
    '''
    if type(x) not in [int, float]:
        raise TypeError('x must be of type int or float.')
    y = x
    return y

if __name__ == '__main__':
    doctest.testmod()
