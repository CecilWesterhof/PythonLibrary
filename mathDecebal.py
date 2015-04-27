import timeit

from utilDecebal import memoize


def fibonacci(n):
    """
    Standard recursive way of defining Fibonacci
    Becomes expensive very fast
    """

    if n < 0:
        raise ValueError, 'Parameter cannot be negative'
    elif (n == 0) or (n == 1):
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

@memoize
def fibonacci_memoize(n):
    """
    Recursive way with memoize of defining Fibonacci
    When called without a parameter it clears the cache
    """

    if n < 0:
        raise ValueError, 'Parameter cannot be negative'
    elif (n == 0) or (n == 1):
        return n
    else:
        return fibonacci_memoize(n - 1) + fibonacci_memoize(n - 2)

def fibonacci_memoize_after_clearing(n):
    """
    Calls fibonacci_memoize after clearing the cache
    Especially useful for testing the performance of fibonacci_memoize
    """

    fibonacci_memoize()
    fibonacci_memoize(n)

def time_function(name, n, description = ''):
    """
    Helper function to test the performance of functions
    """

    if description == '':
        description = name
    print 'Timing {0}({1})'.format(description, n)
    print(timeit.timeit('{0}({1})'.format(name, n),
                        setup   = 'from mathDecebal import {0}'.format(name),
                        number  = 100))


if __name__ == '__main__':
    for n in range(15, 36, 5):
        time_function('fibonacci', n)
    print
    for n in range(15, 36, 5):
        time_function('fibonacci_memoize_after_clearing', n,
                      'fibonacci_memoize')
    print
    for n in range(310, 335, 5):
        time_function('fibonacci_memoize_after_clearing', n,
                      'fibonacci_memoize')
    print
