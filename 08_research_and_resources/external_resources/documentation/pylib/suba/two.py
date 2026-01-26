#
# pylib Example (Documentation)
# two.py
#
# The Python Quants GmbH
#
import doctest


def two(x):
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
        >>> two(10)
        20
        >>> two(20)
        40
        >>> two('python')
        Traceback (most recent call last):
            ...
        TypeError: x must be of type int or float.
    '''
    if type(x) not in [int, float]:
        raise TypeError('x must be of type int or float.')
    y = 2 * x
    return y


if __name__ == '__main__':
    doctest.testmod()

