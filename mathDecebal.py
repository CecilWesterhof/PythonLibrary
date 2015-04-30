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


def lucky_numbers(n):
    """
    Lucky numbers from 1 up-to n
    http://en.wikipedia.org/wiki/Lucky_number
    """

    if n < 3:
        return [1]
    sieve = range(1, n + 1, 2)
    sieve_index = 1
    while True:
        sieve_len   = len(sieve)
        if (sieve_index + 1) > sieve_len:
            break
        skip_count  = sieve[sieve_index]
        if sieve_len < skip_count:
            break
        del sieve[skip_count - 1 : (sieve_len // skip_count) * skip_count : skip_count]
        sieve_index += 1
    return sieve


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
    print('Testing fibonacci')
    fibonacci_numbers = [
        0,       1,        1,        2,       3,
        5,       8,        13,       21,      34,
        55,      89,       144,      233,     377,
        610,     987,      1597,     2584,    4181,
        6765,    10946,    17711,    28657,   46368,
        75025,   121393,   196418,   317811,  514229,
        832040,  1346269,  2178309,  3524578, 5702887,
        9227465, 14930352, 24157817, 39088169
    ]
    error = False
    print('Calculating the fibonacci values 0 to {0}'.
          format(len(fibonacci_numbers) - 1))
    for i in range(len(fibonacci_numbers)):
        if fibonacci_iterative(i) != fibonacci_numbers[i]:
            print('Error calculating fibonacci_iterative({0})'.format(i))
            error = True
        if fibonacci_memoize(i) != fibonacci_numbers[i]:
            print('Error calculating fibonacci_memoize({0})'.format(i))
            error = True
        if fibonacci_old(i) != fibonacci_numbers[i]:
            print('Error calculating fibonacci_old({0})'.format(i))
            error = True
    if not error:
        print('Calculating valuses OK')
    print('')
    repeats = 100
    print('Start with the time needed to calculate {0} times'.format(repeats))
    for n in range(15, 36, 5):
        time_function('fibonacci_old', n, repeats)
    print('')
    for n in range(15, 36, 5):
        time_function('fibonacci_memoize_after_clearing', n, repeats,
                      'fibonacci_memoize')
    print('')
    for n in range(15, 36, 5):
        time_function('fibonacci_iterative', n, repeats)
    print('')
    for n in range(310, 331, 5):
        time_function('fibonacci_memoize_after_clearing', n, repeats,
                      'fibonacci_memoize')
    print('')
    for n in range(310, 331, 5):
        time_function('fibonacci_iterative', n, repeats)
    print('')

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
    print('')

    print('Testing lucky numbers')
    lucky_numbers_list = [
        1,   3,   7,   9,   13,  15,  21,  25,  31,  33,
        37,  43,  49,  51,  63,  67,  69,  73,  75,  79,
        87,  93,  99,  105, 111, 115, 127, 129, 133, 135,
        141, 151, 159, 163, 169, 171, 189, 193, 195, 201,
        205, 211, 219, 223, 231, 235, 237, 241, 259, 261,
        267, 273, 283, 285, 289, 297, 303, 307, 319, 321,
        327, 331, 339, 349, 357, 361, 367, 385, 391, 393,
        399, 409, 415, 421, 427, 429, 433, 451, 463, 475,
        477, 483, 487, 489, 495, 511, 517, 519, 529, 535,
        537, 541, 553, 559, 577, 579, 583, 591, 601, 613,
        615, 619, 621, 631, 639, 643, 645, 651, 655, 673,
        679, 685, 693, 699, 717, 723, 727, 729, 735, 739,
        741, 745, 769, 777, 781, 787, 801, 805, 819, 823,
        831, 841, 855, 867, 873, 883, 885, 895, 897, 903,
        925, 927, 931, 933, 937, 957, 961, 975, 979, 981,
        991, 993, 997,
    ]
    error = False
    for i in range(1, len(lucky_numbers_list)):
        # Value at lucky_numbers_list[i] has to give list including lucky_numbers_list[i]
        check_value = lucky_numbers_list[i]
        if lucky_numbers(check_value) != lucky_numbers_list[:i + 1]:
            print('lucky_numbers({0}) does not calculate correctely'.format(check_value))
            error = True
        check_value -= 1
        # Value lucky_numbers_list[i] -1 has to give list excluding lucky_numbers_list[i]
        if lucky_numbers(check_value) != lucky_numbers_list[:i]:
            print('lucky_numbers({0}) does not calculate correctely'.format(check_value))
            error = True
    if not error:
        print('lucky_numbers OK')
    print('')
