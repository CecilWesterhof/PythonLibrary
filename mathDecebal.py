# This Python file uses the following encoding: utf-8
"""Some math functions"""

from __future__     import print_function

import getopt
import sys

import utilDecebal

from os.path        import split
from timeit         import timeit

from utilDecebal    import memoize


##### Functions

def factorial_iterative(x):
    assert x >= 0
    result = 1
    for i in range(2, x + 1):
        result *= i
    return result

def factorial_recursive(x, y = 1, z = 1):
    assert x >= 0
    if x < 2:
        return y
    return y if z > x else factorial_recursive(x, z * y, z + 1)

def factorial_recursive_old(x, y = 1):
    assert x >= 0
    if x < 2:
        return y
    return factorial_recursive_old(x - 1, x * y)

def factorial_tail_recursion(x):
    assert x >= 0
    y = 1
    z = 1
    if x < 2:
        return y
    while True:
        if z > x:
            return y
        y *= z
        z += 1

def factorial_tail_recursion_old(x):
    assert x >= 0
    y = 1
    if x < 2:
        return y
    while True:
        if x == 1:
            return y
        y *= x
        x -= 1

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

    assert n >= 0
    if (n == 0) or (n == 1):
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

    assert n >= 0
    if (n == 0) or (n == 1):
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

    assert n >= 0
    if (n == 0) or (n == 1):
        return n
    else:
        return fibonacci_old(n - 1) + fibonacci_old(n - 2)

def happy_number(n):
    """
    Check if a number is a happy number
    https://en.wikipedia.org/wiki/Happy_number
    """

    assert n >= 1
    def create_current(n):
        return int(''.join(sorted(str(n))))


    global _happy_set
    global _unhappy_set

    run     = set()
    current = create_current(n)
    while True:
        if (current in run) or (current in _unhappy_set):
            _unhappy_set |= run
            return False
        if current in _happy_set:
            _happy_set |= run
            return True
        run.add(current)
        current = create_current(sum([_squares[value] for value in str(current)]))

def happy_numbers_count(n):
    assert n >= 1
    count = 0

    for i in range(1, n + 1):
        if happy_number(i):
            count += 1
    return count

# By making this a function it is possible to reset the values for testing purposes
def happy_number_init():
    global _happy_set
    global _squares
    global _unhappy_set

    _happy_set      = { 1 }
    _unhappy_set    = set()
    _squares        = dict((str(i), i*i) for i in range(1, 10))

def happy_numbers_list(n):
    assert n >= 1
    found = []

    for i in range(1, n + 1):
        if happy_number(i):
            found.append(i)
    return found

def lucky_numbers(n):
    """
    Lucky numbers from 1 up-to n
    http://en.wikipedia.org/wiki/Lucky_number
    """

    assert n >= 1
    if n < 3:
        return [1]
    sieve = list(range(1, n + 1, 2))
    sieve_index = 1
    while True:
        sieve_len   = len(sieve)
        if (sieve_index + 1) > sieve_len:
            break
        skip_count  = sieve[sieve_index]
        if sieve_len < skip_count:
            break
        del sieve[skip_count - 1 : : skip_count]
        sieve_index += 1
    return sieve

def lucky_numbers_count(n):
    return len(lucky_numbers(n))


##### Test functions

def time_function(name, n, repeats, notifier, description = '', display = True):
    """
    Helper function to test the performance of functions
    """

    if display:
        if description == '':
            description = name
        notifier.give_msg('Timing {0}({1}): '.format(description, n),
                          use_newline = False)
    used_time = timeit('{0}({1})'.format(name, n),
                       setup   = 'from mathDecebal import {0}'.format(name),
                       number  = repeats)
    if display:
        print('{0:.3E}'.format(used_time))
    return used_time


##### Init

happy_number_init()

### Testing should go to its own file
### Testing and performance checking (if not part of testing) should be splitted
if __name__ == '__main__':
    keywords        = [
        'all',
        'factorial',
        'factorial-long',
        'fibonacci',
        'happy',
        'lucky',
    ]
    keywords_msg    = [
        '--all',
        '--factorial',
        '--factorial-long',
        '--fibonacci',
        '--happy',
        '--lucky',
    ]
    notify          = utilDecebal.TimedMessage()
    (options,
     extraParams)   = getopt.getopt(sys.argv[1:], '', keywords)
    progname        = split(sys.argv[0])[1]

    if len(options) > 1 or len(extraParams) != 0:
        error   = '{0}: Wrong parameters ({1})'. \
                  format(progname, ' '.join(sys.argv[1:]))
        usage   = '    {0} {1}'.format(progname, ' | '.join(keywords_msg))
        print(error, file = sys.stderr)
        print(usage, file = sys.stderr)
        sys.exit(1)

    do_all = do_factorial = do_fibonacci = do_happy = do_lucky = False
    if len(options) == 0:
        do_all = True
    else:
        action = options[0][0]
        if   action == '--all':
            do_all              = True
        elif action == '--factorial':
            do_factorial        = True
            do_factorial_long   = False
        elif action == '--factorial-long':
            do_factorial        = True
            do_factorial_long   = True
        elif action == '--fibonacci':
            do_fibonacci        = True
        elif action == '--happy':
            do_happy            = True
        elif action == '--lucky':
            do_lucky            = True
        else:
            print(progname + ': Unhandled parameter ' + action,
                  file = sys.stderr)
            sys.exit(1)

    if do_all or do_factorial:
        notify.give_msg('Testing factorial')
        factorial_numbers = [
            1,                    1,                      2,
            6,                    24,                     120,
            720,                  5040,                   40320,
            362880,               3628800,                39916800,
            479001600,            6227020800,             87178291200,
            1307674368000,        20922789888000,         355687428096000,
            6402373705728000,     121645100408832000,     2432902008176640000,
            51090942171709440000, 1124000727777607680000,
        ]
        error = False
        notify.give_msg('Check if the functions give the right value for the first '
                        '{0} values'.format(len(factorial_numbers)))
        for i in range(len(factorial_numbers)):
            if factorial_iterative(i) != factorial_numbers[i]:
                notify.give_msg('Error calculating factorial_iterative({0})'
                                '{1} instead of {2}'.
                                format(i, factorial_iterative(i), factorial_numbers[i]))
                error = True
            if factorial_recursive(i) != factorial_numbers[i]:
                notify.give_msg('Error calculating factorial_recursive({0}): '
                                '{1} instead of {2}'.
                                format(i, factorial_recursive(i), factorial_numbers[i]))
                error = True
            if factorial_recursive_old(i) != factorial_numbers[i]:
                notify.give_msg('Error calculating factorial_recursive_old({0})'
                                '{1} instead of {2}'.
                                format(i, factorial_recursive_old(i), factorial_numbers[i]))
                error = True
            if factorial_tail_recursion(i) != factorial_numbers[i]:
                notify.give_msg('Error calculating factorial_tail_recursion({0}): '
                                '{1} instead of {2}'.
                                format(i, factorial_tail_recursion(i), factorial_numbers[i]))
                error = True
            if factorial_tail_recursion_old(i) != factorial_numbers[i]:
                notify.give_msg('Error calculating factorial_tail_recursion_old({0})'
                                '{1} instead of {2}'.
                                format(i, factorial_tail_recursion_old(i), factorial_numbers[i]))
                error = True
        start   = len(factorial_numbers)
        end     = 985
        notify.give_msg('Check that all version gives the same values for {0} upto {1}'.
                      format(start, end))
        for i in range(start, end + 1):
            factorial_iter      = factorial_iterative(i)
            factorial_recur     = factorial_recursive(i)
            factorial_recur_old = factorial_recursive_old(i)
            factorial_tail      = factorial_tail_recursion(i)
            factorial_tail_old  = factorial_tail_recursion_old(i)
            if factorial_iter != factorial_recur:
                notify.give_msg('factorial_iterative({0}) not equal factorial_recursive({0}):'
                                '{1}, {2}'.format(i, factorial_iter, factorial_recur))
                error = True
            if factorial_iter != factorial_recur_old:
                notify.give_msg('factorial_iterative({0}) not equal factorial_recursive_old({0}):'
                                '{1}, {2}'.format(i, factorial_iter, factorial_recur_old))
                error = True
            if factorial_iter != factorial_tail:
                notify.give_msg('factorial_iterative({0}) not equal factorial_tail_recursion({0}):'
                                '{1}, {2}'.format(i, factorial_iter, factorial_tail))
                error = True
            if factorial_iter != factorial_tail_old:
                notify.give_msg('factorial_iterative({0}) not equal factorial_tail_recursion_old({0}):'
                                '{1}, {2}'.format(i, factorial_iter, factorial_tail_old))
                error = True
        start   = 1000
        end     = 100000
        step    = 1000
        notify.give_msg('Check that the non recursive variants give the same value '
                        'from {0} upto {1} step {2}'.format(start, end, step))
        for i in range(start, end + 1, step):
            if (i % 10000) == start:
                notify.give_msg('Currently at %7d' % i)
            factorial_iter      = factorial_iterative(i)
            factorial_tail      = factorial_tail_recursion(i)
            factorial_tail_old  = factorial_tail_recursion_old(i)
            if factorial_iter != factorial_tail:
                notify.give_msg('factorial_iterative({0}) not equal factorial_tail_recursion({0}):'
                                '{1}, {2}'.format(i, factorial_iter, factorial_tail))
                error = True
            if factorial_iter != factorial_tail_old:
                notify.give_msg('factorial_iterative({0}) not equal factorial_tail_recursion_old({0}):'
                                '{1}, {2}'.format(i, factorial_iter, factorial_tail_old))
                error = True
        if not error:
            notify.give_msg('Calculating values OK')
        print('')
        repeats = 100000
        notify.give_msg('Start with the time needed to calculate {0} times'.format(repeats))
        for function in [
                'factorial_iterative         ',
                'factorial_recursive         ',
                'factorial_recursive_old     ',
                'factorial_tail_recursion    ',
                'factorial_tail_recursion_old',
        ]:
            time_function(function, 985, repeats, notify)
        print('')
        repeats = 1
        notify.give_msg('Start with the time needed to calculate {0} times'.format(repeats))
        notify.give_msg('No recursive, because without tail recursion you would run '
                        'out of stack space', show_time = False)
        start   = 10 ** 5
        step    = 10 ** 5
        if do_factorial and do_factorial_long:
            end = 10 ** 6
        else:
            end = 5 * 10 ** 5
        for i in range(start, end + 1, step):
            for function in [
                    'factorial_iterative         ',
                    'factorial_tail_recursion    ',
                    'factorial_tail_recursion_old',
            ]:
                time_function(function, i, repeats, notify)
            print('')
        notify.give_msg('These result show that tail recursion can be interesting')
        notify.give_msg('They show also that the way you use tail recursion is important',
                        show_time = False)
        print('')

    if do_all or do_fibonacci:
        notify.give_msg('Testing fibonacci')
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
        notify.give_msg('Calculating the fibonacci values 0 to {0}'.
                      format(len(fibonacci_numbers) - 1))
        for i in range(len(fibonacci_numbers)):
            if fibonacci_iterative(i) != fibonacci_numbers[i]:
                notify.give_msg('Error calculating fibonacci_iterative({0})'.format(i))
                error = True
            if fibonacci_memoize(i) != fibonacci_numbers[i]:
                notify.give_msg('Error calculating fibonacci_memoize({0})'.format(i))
                error = True
            if fibonacci_old(i) != fibonacci_numbers[i]:
                notify.give_msg('Error calculating fibonacci_old({0})'.format(i))
                error = True
        start   = 50
        end     = 10 ** 6
        step    = 50000
        notify.give_msg('Check that fibonacci_iter and fibonacci_memoize give '
                        'the same values for {0} upto {1} step {2}'.
                        format(start, end, step))
        for i in range(start, end + 1, step):
            if (i % 100000) == start:
                notify.give_msg('Currently at %7d' % i)
            fibonacci_iter       = fibonacci_iterative(i)
            fibonacci_memoize    = fibonacci_iterative(i)
            if fibonacci_iter != fibonacci_memoize:
                notify.give_msg('fibonacci_iterative({0}) not equal fibonacci_memoize({0}):'
                                '{1}, {2}'.format(i, fibonacci_iter, fibonacci_memoize))
                error = True
        if not error:
            notify.give_msg('Calculating values OK')
        print('')
        repeats = 100
        notify.give_msg('Start with the time needed to calculate {0} times'.format(repeats))
        for n in range(15, 36, 5):
            time_function('fibonacci_old', n, repeats, notify)
        print('')
        for n in range(15, 36, 5):
            time_function('fibonacci_memoize_after_clearing', n, repeats, notify,
                          'fibonacci_memoize')
        print('')
        for n in range(15, 36, 5):
            time_function('fibonacci_iterative', n, repeats, notify)
        print('')
        for n in range(310, 331, 5):
            time_function('fibonacci_memoize_after_clearing', n, repeats, notify,
                          'fibonacci_memoize')
        print('')
        for n in range(310, 331, 5):
            time_function('fibonacci_iterative', n, repeats, notify)
        print('')

        for large_fibonacci in range(20, 41, 5):
            notify.give_msg(
                'Calculating fibonacci_old, fibonacci_memoize and '
                'fibonacci_iterative')
            notify.give_msg(
                'once for {0} to determine speed increase'.
                format(large_fibonacci),
                show_time = False)
            time_fibonacci_old  = time_function('fibonacci_old', large_fibonacci, 1, notify,
                                                display = False)
            time_fibonacci_mem  = time_function('fibonacci_memoize_after_clearing',
                                                large_fibonacci, 1, notify,
                                                display = False)
            time_fibonacci_iter = time_function('fibonacci_iterative',
                                                large_fibonacci, 1, notify,
                                                display = False)
            notify.give_msg('Increase old     -> memoize   {0:.3E}'.
                            format(int(time_fibonacci_old / time_fibonacci_mem)))
            notify.give_msg('({0:.3E} / {1:.3E})'.
                            format(time_fibonacci_old, time_fibonacci_mem),
                            show_time = False)
            notify.give_msg('Increase memoize -> iterative {0:.3E}'.
                            format(int(time_fibonacci_mem / time_fibonacci_iter)))
            notify.give_msg('({0:.3E} / {1:.3E})'.
                            format(time_fibonacci_mem, time_fibonacci_iter),
                            show_time = False)
            print('')
        large_fibonacci = 330
        notify.give_msg(
            'Calculating fibonacci_memoize and fibonacci_iterative')
        notify.give_msg(
            'once for {0} to determine speed increase'.
            format(large_fibonacci),
            show_time = False)
        time_fibonacci_mem  = time_function('fibonacci_memoize_after_clearing',
                                            large_fibonacci, 1, notify,
                                            display = False)
        time_fibonacci_iter = time_function('fibonacci_iterative',
                                            large_fibonacci, 1, notify,
                                            display = False)
        notify.give_msg('Increase memoize -> iterative {0}'.
                        format(int(time_fibonacci_mem / time_fibonacci_iter)))
        notify.give_msg('({0:.3E} / {1:.3E})'.
                        format(time_fibonacci_mem, time_fibonacci_iter),
                        show_time = False)
        print('')
        notify.give_msg(
            'The best fibonacci is the iterative version: '
            'it is about 10 times faster.')
        notify.give_msg(
            'With fibonacci_iterative you can also calculate big numbers.',
            show_time = False)
        notify.give_msg(
            'When none has been calculated the biggest you can calculte with '
            'fibonacci_memoize is 332.',
            show_time = False)
        notify.give_msg('fibonacci_iterative(500):', show_time = False)
        notify.give_msg('{0}'.format(fibonacci_iterative(500)),
                        show_time = False)
        notify.give_msg('That is why fibonacci calls fibonacci_iterative.',
                        show_time = False)
        print('')

    if do_all or do_happy:
        notify.give_msg('Testing happy numbers')
        notify.give_msg('Checking the first 1000 numbers', show_time = False)
        happy_numbers = [
            1,   7,   10,  13,  19,  23,  28,  31,  32,  44,
            49,  68,  70,  79,  82,  86,  91,  94,  97,  100,
            103, 109, 129, 130, 133, 139, 167, 176, 188, 190,
            192, 193, 203, 208, 219, 226, 230, 236, 239, 262,
            263, 280, 291, 293, 301, 302, 310, 313, 319, 320,
            326, 329, 331, 338, 356, 362, 365, 367, 368, 376,
            379, 383, 386, 391, 392, 397, 404, 409, 440, 446,
            464, 469, 478, 487, 490, 496, 536, 556, 563, 565,
            566, 608, 617, 622, 623, 632, 635, 637, 638, 644,
            649, 653, 655, 656, 665, 671, 673, 680, 683, 694,
            700, 709, 716, 736, 739, 748, 761, 763, 784, 790,
            793, 802, 806, 818, 820, 833, 836, 847, 860, 863,
            874, 881, 888, 899, 901, 904, 907, 910, 912, 913,
            921, 923, 931, 932, 937, 940, 946, 964, 970, 973,
            989, 998, 1000
        ]
        if happy_numbers_list(1000) == happy_numbers:
            notify.give_msg('Happy numbers OK')
        else:
            notify.give_msg('ERROR in happy list')
            error = True
        print('')
        count = 10 ** 8
        time_function('happy_numbers_list', count, 1, notify)
        notify.give_msg('Calculating happy_numbers_count({0})'.format(count))
        notify.give_msg(str(happy_numbers_count(count)))
        print('')

    if do_all or do_lucky:
        notify.give_msg('Testing lucky numbers')
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
        if lucky_numbers(lucky_numbers_list[-1]) != lucky_numbers_list:
            notify.give_msg('ERROR in lucky list')
            error = True
        if not error:
            notify.give_msg('lucky_numbers OK')
        print('')
        count = 10 ** 8
        time_function('lucky_numbers', count, 1, notify)
        notify.give_msg('Calculating lucky_numbers_count({0})'.format(count))
        notify.give_msg(str(lucky_numbers_count(count)))
        print('')
