#
# pylib Example (Documentation)
#
# The Python Quants GmbH
#
import doctest

def three(x):
    ''' Simple function.

    :Parameters:
        x: float
            input number

    :Returns:
        y: float
            output number, 3 * x

    :Raise:
        TypeError
            if x is not a number

    :Examples:
        >>> three(10)
        30
        >>> three(20)
        60
        >>> three('python')
        Traceback (most recent call last):
            ...
        TypeError: x must be of type int or float.
    '''
    if type(x) not in [int, float]:
        raise TypeError('x must be of type int or float.')
    return 3 * x


if __name__ == '__main__':
    doctest.testmod()

