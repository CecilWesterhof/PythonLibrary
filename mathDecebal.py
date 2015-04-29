# This Python file uses the following encoding: utf-8
"""Some math functions"""

import sys

from timeit import timeit

from utilDecebal import memoize


##### Functions

def fibonacci(n):
    """
    Calculates fibonacci number, uses fibonacci_iterative
    """

    fibonacci_iterative(n)

def fibonacci_iterative(n):
    """
    Iterative way of calculating fibonacci
    Less clear as recursive way, but can be called with 500
    Is also ten to fifteen times as fast as memoized recursive version
    """

    if n < 0:
        raise ValueError('Parameter cannot be negative')
    elif (n == 0) or (n == 1):
        return n
    else:
        a, b = 0, 1
        for i in range(0, n):
            a, b = b, a + b
        return a

@memoize
def fibonacci_memoize(n):
    """
    Recursive way with memoize of defining Fibonacci
    When called without a parameter it clears the cache
    """

    if n < 0:
        raise ValueError('Parameter cannot be negative')
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
    return fibonacci_memoize(n)

def fibonacci_old(n):
    """
    Standard recursive way of defining Fibonacci
    Becomes expensive very fast
    """

    if n < 0:
        raise ValueError('Parameter cannot be negative')
    elif (n == 0) or (n == 1):
        return n
    else:
        return fibonacci_old(n - 1) + fibonacci_old(n - 2)


##### Test functions

def time_function(name, n, repeats, description = '', display = True):
    """
    Helper function to test the performance of functions
    """

    if display:
        if description == '':
            description = name
        sys.stdout.write('Timing {0}({1}): '.format(description, n))
        sys.stdout.flush()
    used_time = timeit('{0}({1})'.format(name, n),
                       setup   = 'from mathDecebal import {0}'.format(name),
                       number  = repeats)
    if display:
        print(used_time)
    return used_time


##### Init

if __name__ == '__main__':
    # print('Testing fibonacci')
    # repeats = 100
    # print('Start with the time needed to calculate {0} times'.format(repeats))
    # for n in range(15, 36, 5):
    #     time_function('fibonacci_old', n, repeats)
    # print('')
    # for n in range(15, 36, 5):
    #     time_function('fibonacci_memoize_after_clearing', n, repeats,
    #                   'fibonacci_memoize')
    # print('')
    # for n in range(15, 36, 5):
    #     time_function('fibonacci_iterative', n, repeats)
    # print('')
    # for n in range(310, 331, 5):
    #     time_function('fibonacci_memoize_after_clearing', n, repeats,
    #                   'fibonacci_memoize')
    # print('')
    # for n in range(310, 331, 5):
    #     time_function('fibonacci_iterative', n, repeats)
    # print('')

    for large_fibonacci in range(20, 41, 5):
        print(
            'Calculating fibonacci_old, fibonacci_memoize and '
            'fibonacci_iterative once for {0} to determine speed increase'.
            format(large_fibonacci))
        time_fibonacci_old  = time_function('fibonacci_old', large_fibonacci, 1,
                                            display = False)
        time_fibonacci_mem  = time_function('fibonacci_memoize_after_clearing',
                                            large_fibonacci, 1,
                                            display = False)
        time_fibonacci_iter = time_function('fibonacci_iterative',
                                            large_fibonacci, 1,
                                            display = False)
        print('Increase old     -> memoize   {0} ({1} / {2})'.
              format(int(time_fibonacci_old / time_fibonacci_mem),
                     time_fibonacci_old, time_fibonacci_mem))
        print('Increase memoize -> iterative {0} ({1} / {2})'.
              format(int(time_fibonacci_mem / time_fibonacci_iter),
                     time_fibonacci_mem, time_fibonacci_iter))
        print('')
    for large_fibonacci in range(310, 331, 5):
        print(
            'Calculating fibonacci_memoize and fibonacci_iterative once for {0} '
            'to determine speed increase'.format(large_fibonacci))
        time_fibonacci_mem  = time_function('fibonacci_memoize_after_clearing',
                                            large_fibonacci, 1,
                                            display = False)
        time_fibonacci_iter = time_function('fibonacci_iterative',
                                            large_fibonacci, 1,
                                            display = False)
        print('Increase memoize -> iterative {0} ({1} / {2})'.
              format(int(time_fibonacci_mem / time_fibonacci_iter),
                     time_fibonacci_mem, time_fibonacci_iter))
        print('')

    print(
        'The best fibonacci is the iterative version: '
        'it is about 15 times faster.\n'
        'With fibonacci_iterative you can also calculate big numbers.\n'
        'When none has been calculated the biggest you can calculte with '
        'fibonacci_memoize is 332.\n'
        'fibonacci_iterative(500):\n{0}\n'
        'That is why fibonacci calls fibonacci_iterative.'.
        format(fibonacci_iterative(500)))
