# This Python file uses the following encoding: utf-8
"""Some utilty functions that could be handy"""

##### Classes

class MovingAverage:
    """
    http://en.wikipedia.org/wiki/Moving_average

    This is an implementation of moving average in Python.

    Moving average gives in the normal definition only a value when there
    are ate least LENGTH values. My implementation gives always a result.
    You can always ignore the first LENGTH - 1 values.

    An extension would be to accept all numeric types.
    """
    def next_value(self, next):
        if not (isinstance(next, int) or isinstance(next, float)):
            raise TypeError('Parameter has to be (subclasss of) float or int')
        self._current_total += next
        self._old_values.append(next)
        if len(self._old_values) > self._length:
            self._current_total -= self._old_values.pop(0)
        if (self._current_total == float("inf")) or \
           (self._current_total == float("-inf")):
            raise OverflowError(
                "Can not give a value because there was an overflow")
        return self._current_total / len(self._old_values)

    def __init__(self, length):
        if not isinstance(length, int):
            raise TypeError("Length should be integral")
        if length < 2:
            raise ValueError, 'Parameter should be greater or equal 2'
        self._length            = length
        self._old_values        = []
        self._current_total     = 0.0


##### Functions

# In Clojure you have the memoize function
# to cache values that need a long time to be computed
# I implemented a Python version
#
# If the value is already cached,
# that value is returned
# otherwise the value is calculate, cached and returned
#
# When called without a parameter the cache is emptied
# Useful for testing performance with timeit
# Description of its usefulness in memoize.md
def memoize(function):
    """
    Just put '@memoize' before a long running function like:
    @memoize
    def long_running_function(n):
    .
    .
    .
    """

    # Initialy nothing cached
    S = {}

    def wrapping_function(*args):
        """
        This function will replace the function that is memoized
        When called without parameters it empties the cache
        """
        if len(args) == 0:
            S.clear()
            return None
        # When not cached calculate and cache
        if args not in S:
            S[args] = function(*args)
        # return cached value
        return S[args]

    return wrapping_function


##### Test functions

def test_moving_average(length, input_array, output_array):
    if len(input_array) != len(output_array):
        raise ValueError, \
            'Arrays have different lengths. Input: {0}, output: {1}.'. \
            format(len(input_array), len(output_array))

    print('Moving Average length {0}:'.format(length))
    average = MovingAverage(length)
    error   = False
    for i in range(length):
        expected    = output_array[i]
        expected2   = sum(input_array[max(0, i + 1 - length):i + 1]) \
                      * 1. / min(length, i + 1)
        gotten      = average.next_value(input_array[i])
        if gotten != expected2:
            print('Moving average: {0}, slice {1}, for slice {2}'. \
                format(gotten, expected2, i + 1))
            error = True
        if str(gotten) != expected:
            print('Got {0} instead of {1} for the {2} value'. \
                format(gotten, expected, i))
            error = True
    if not error:
        print('Moving average OK for length {0}'.format(length))


##### Init

if __name__ == '__main__':
    from timeit import timeit

    # For testing memoize, if someone has a better idea …
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

    print('Testing memoize with fibonacci')
    Error = False
    time_fibonacci      = timeit('fibonacci(40)',
                                 setup   = 'from __main__ import fibonacci',
                                 number  = 1)
    time_fibonacci_mem  = timeit('fibonacci_memoize(40)',
                                 setup   = 'from __main__ import fibonacci_memoize',
                                 number  = 1)
    # In my tests mostly above 750000, but build in a safety margin
    # It shows that memoize can be interesting indeed
    speedup = 700000
    if time_fibonacci / time_fibonacci_mem < speedup:
        print('Looks like memoize does not work correctly')
        print('fibonacci_memoize should be {0} times faster as fibonacci'. \
            format(speedup))
        print('It was only {0} times faster ({1} / {2})'. \
            format(time_fibonacci / time_fibonacci_mem, \
                   time_fibonacci, \
                   time_fibonacci_mem))
        Error = True
    if not Error:
        print('Memoize OK')
    print time_fibonacci, time_fibonacci_mem, time_fibonacci / time_fibonacci_mem
    print

    # For testing moving average, if someone wants to give real big sets …
    input06 = [
        20.0, 22.0, 21.0, 24.0, 24.0, 23.0, 25.0, 26.0, 20.0, 24.0,
        26.0, 26.0, 25.0, 27.0, 28.0, 27.0, 29.0, 27.0, 25.0, 24.0,
    ]
    output06 = [
        '20.0',          '21.0',          '21.0',          '21.75',         '22.2',
        '22.3333333333', '23.1666666667', '23.8333333333', '23.6666666667', '23.6666666667',
        '24.0',          '24.5',          '24.5',          '24.6666666667', '26.0',
        '26.5',          '27.0',          '27.1666666667', '27.1666666667', '26.6666666667',
    ]
    input10 = [
        20.0, 22.0, 24.0, 25.0, 23.0, 26.0, 28.0, 26.0, 29.0, 27.0,
        28.0, 30.0, 27.0, 29.0, 28.0,
    ]
    output10 = [
        '20.0',          '21.0',          '22.0',          '22.75',         '22.8',
        '23.3333333333', '24.0',          '24.25',         '24.7777777778', '25.0',
        '25.8',          '26.6',          '26.9',          '27.3',          '27.8',
    ]

    test_moving_average( 6, input06, output06)
    test_moving_average(10, input10, output10)
    print
