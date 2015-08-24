# This Python file uses the following encoding: utf-8
'''Some utilty classes and functions that could be handy'''

import functools
import json
import marshal
import os
import pickle
import re
import sys

from os.path    import expanduser
from platform   import python_version
from time       import sleep, strftime, time

if python_version()[0] < '3':
    from urllib         import urlopen
else:
    from urllib.request import urlopen


##### Exception Classes

class SerializationError(Exception):
    pass


##### Classes

### Improvements
### Create a next_values
### Create a internal checking function
### Implement no_rolling_sum
### Expand testing
### Option to force no_rolling_sum when no_rolling_sum is False
### - for the current call
### - for the current call and length -1 following
class MovingAverage:
    '''
    http://en.wikipedia.org/wiki/Moving_average

    This is an implementation of moving average in Python.

    Moving average gives in the normal definition only a value when there
    are ate least LENGTH values. My implementation gives always a result.
    You can always ignore the first LENGTH - 1 values.

    An extension would be to accept all numeric types.
    '''

    def current_value(self):
        '''Return current value, None if no current value'''

        if len(self._old_values) == 0:
            return None
        return self._return_value()

    def next_value(self, next):
        '''Calculate next value and return it'''

        if not (isinstance(next, int) or isinstance(next, float)):
            raise TypeError('Parameter has to be (subclasss of) float or int')
        self._current_total += next
        self._old_values.append(next)
        if len(self._old_values) > self._length:
            self._current_total -= self._old_values.pop(0)
        return self._return_value()

    def _return_value(self):
        '''Return current value'''

        if (self._current_total == float("inf")) or \
           (self._current_total == float("-inf")):
            raise OverflowError(
                "Can not give a value because there was an overflow")
        return self._current_total / len(self._old_values)

    def __init__(self, length):
        '''Initialise the class'''

        if not isinstance(length, int):
            raise TypeError("Length should be integral")
        if length < 2:
            raise ValueError('Parameter should be greater or equal 2')
        self._length            = length
        self._old_values        = []
        self._current_total     = 0.0

### Have the possibility to give the stream instead of using stdout
class TimedMessage:
    '''
    For printing messages with time prepended before it
    Has the possibilty to keep time print blank for when several messages
    are send shortly after eachother.
    Also the possibilty to stay on the same line when things need to be appended
    '''

    def give_msg(self, message, show_time = True, use_newline = True):
        '''
        Prints the message to stdout
        Use show_time = False when you do not want time
        Use use_newline = False if you do not want a newline
        '''

        if show_time:
            time = strftime(self._format)
        else:
            time = self._blank_time
        formatted_message = time + message
        if use_newline:
            print(formatted_message)
        else:
            # To work with Python2 the flush is a seperate statement
            sys.stdout.write(formatted_message)
            sys.stdout.flush()

    def __init__(self, format = '%H:%M:%S: '):
        '''Initialise the class'''

        self._format        = format
        self._blank_time    = ' ' * len(strftime(self._format))


##### Functions

def convert_serialization(format_in, format_out, filename_in, filename_out):
    data_in = get_serialization(format_in, filename_in)
    save_serialization(format_out, data_in, filename_out)
    data_out = get_serialization(format_out, filename_out)
    if data_in != data_out:
        raise SerializationError('Serialization from {0} to {1} not successful'.
                                     format(filename_in, filename_out))

def find(directory, to_match, ignore_case = False):
    to_match =  to_match + r'$'
    if ignore_case:
        p = re.compile(to_match, re.IGNORECASE)
    else:
        p = re.compile(to_match)
    results = []
    for dirpath, dirnames, filenames in os.walk(expanduser(directory)):
        for filename in filenames:
            if p.match(filename):
                results.append(os.path.join(dirpath, filename))
    return results

def get_serialization(format, filename):
    '''General function for getting serialized data'''

    with open(expanduser(filename), 'rb') as in_f:
        return format.load(in_f)

_size_suffixes = {1000: ['KB',  'MB',  'GB',  'TB',  'PB',  'EB',  'ZB',  'YB' ],
                  1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

def human_readable_size(size, binary_form = True, to_large_is_error = True):
    '''
    Convert a file size to human-readable form.
    When binary_form is False use multiplies of 1000 instead of 1024
    Returns: string with human-readable form
    '''

    if size < 0:
        raise ValueError('number must be non-negative')

    if size == 0:
        return '0'
    # Use floats instead of ints to make it work with Python 2
    multiple = 1024. if binary_form else 1000.
    for suffix in _size_suffixes[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)
    if to_large_is_error:
        raise ValueError('number too large')
    return '{0:.1f} {1}'.format(size, suffix)

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
    '''
    Just put '@memoize' before a long running function like:
    @memoize
    def long_running_function(n):
    .
    .
    .
    '''

    # Initialy nothing cached
    S = {}

    def wrapping_function(*args):
        '''
        This function will replace the function that is memoized
        When called without parameters it empties the cache
        '''

        if len(args) == 0:
            S.clear()
            return None
        # When not cached calculate and cache
        if args not in S:
            S[args] = function(*args)
        # return cached value
        return S[args]

    return wrapping_function

def save_serialization(format, data, filename):
    '''General function for serializing data'''

    with open(expanduser(filename), 'wb') as out_f:
        format.dump(data, out_f)

### Extension: instead of printing the needed time return it
def time_fetchURLs(server, URLs, times, wait_between_fetches):
    '''
    Sometimes you need to know the time needed for fetching a sequence of URLs
    For example you want to know how much time loading a page takes
    You can use time_fetchURLs to do this one or more times.
    It needs:
    - server
    - URLs
    - times
    - wait_between_fetches
    '''

    def _read_urls():
        start_time  = time()
        for url in URLs:
            urlopen(server + url).read()
        end_time    = time()
        print('It took {0:.5f} seconds'.format(end_time - start_time))
        sys.stdout.flush()

    if times < 1:
        raise ValueError('You should fetch at least once')
    if wait_between_fetches < 0:
        raise ValueError('You cannot wait a negative time')
    _read_urls()
    for x in range(0, times - 1):
        sleep(wait_between_fetches)
        _read_urls()


##### Test functions

def test_moving_average(length, input_array, output_array, notify):
    '''For testing the functionality of MovingAverage'''

    if len(input_array) != len(output_array):
        raise ValueError(
            'Arrays have different lengths. Input: {0}, output: {1}.'.
            format(len(input_array), len(output_array)))

    notify.give_msg('Moving Average length {0}:'.format(length))
    average = MovingAverage(length)
    error   = False
    if average.current_value() != None:
        notify.give_msg('Starting with current_value did not give None')
        error = True
    for i in range(length):
        expected    = output_array[i]
        expected2   = repr(sum(input_array[max(0, i + 1 - length):i + 1]) \
                      * 1. / min(length, i + 1))
        gotten      = repr(average.next_value(input_array[i]))
        if repr(average.current_value()) != gotten:
            notify.give_msg('current_value does not return last calculated value')
            error = True
        if gotten != expected2:
            notify.give_msg('Moving average: {0}, slice {1}, for slice {2}'. \
                format(gotten, expected2, i + 1))
            error = True
        if gotten != expected:
            notify.give_msg('Got {0} instead of {1} for the {2} value'. \
                format(gotten, expected, i))
            error = True
    if not error:
        notify.give_msg('Moving average OK for length {0}'.format(length))


##### Init

_all_serialization_formats           = [json, pickle, marshal]
_convert_to_serialization_formats    = [json, pickle]

for format_in in _all_serialization_formats:
    # Create save functions
    globals()[
        'save_%s' % (format_in.__name__)
    ] = functools.partial(save_serialization, format_in)
    # Create get functions
    globals()[
        'get_%s' % (format_in.__name__)
    ] = functools.partial(get_serialization, format_in)
    # Create functions to convert from one format to another
    for format_out in _convert_to_serialization_formats:
        # No use to convert to yourself
        if format_in == format_out:
            continue
        globals()[
            '%s_to_%s' % (format_in.__name__, format_out.__name__)
        ] = functools.partial(convert_serialization, format_in, format_out)

del format_in, format_out


if __name__ == '__main__':
    from timeit import timeit

    notify          = TimedMessage()

    # For testing memoize, if someone has a better idea …
    def fibonacci(n):
        '''
        Standard recursive way of defining Fibonacci
        Becomes expensive very fast
        '''

        if n < 0:
            raise ValueError('Parameter cannot be negative')
        elif (n == 0) or (n == 1):
            return n
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)

    @memoize
    def fibonacci_memoize(n):
        '''
        Recursive way with memoize of defining Fibonacci
        When called without a parameter it clears the cache
        '''

        if n < 0:
            raise ValueError('Parameter cannot be negative')
        elif (n == 0) or (n == 1):
            return n
        else:
            return fibonacci_memoize(n - 1) + fibonacci_memoize(n - 2)

    speedup             = 7 * 10 ** 5
    notify.give_msg('Testing if fibonacci(40) is at least {0:.3E} times faster with memoize'.
                    format(speedup))
    Error               = False
    time_fibonacci      = timeit('fibonacci(40)',
                                 setup   = 'from __main__ import fibonacci',
                                 number  = 1)
    time_fibonacci_mem  = timeit('fibonacci_memoize(40)',
                                 setup   = 'from __main__ import fibonacci_memoize',
                                 number  = 1)
    # In my tests mostly above 750000, but build in a safety margin
    # It shows that memoize can be interesting indeed
    if time_fibonacci / time_fibonacci_mem < speedup:
        notify.give_msg('Looks like memoize does not work correctly')
        notify.give_msg('It was only {0:.3E} times faster ({1:.3E} / {2:.3E})'.
            format(time_fibonacci / time_fibonacci_mem,
                   time_fibonacci, time_fibonacci_mem),
            show_time = False)
        Error = True
    if not Error:
        notify.give_msg('Memoize OK: {0:.3E} times faster  ({1:.3E} / {2:.3E})'.
                        format(time_fibonacci / time_fibonacci_mem,
                               time_fibonacci, time_fibonacci_mem))
    print('')

    size = 0
    print(human_readable_size(size, False))
    print(human_readable_size(size))
    for i in range(27):
        size = 10 ** i
        print(human_readable_size(size, False))
        print(human_readable_size(size))

    # For testing moving average, if someone wants to give real big sets …
    input06 = [
        20.0, 22.0, 21.0,
        24.0, 24.0, 23.0,
        25.0, 26.0, 20.0,
        24.0, 26.0, 26.0,
        25.0, 27.0, 28.0,
        27.0, 29.0, 27.0,
        25.0, 24.0,
    ]
    output06 = [
        '20.0',               '21.0',               '21.0',
        '21.75',              '22.2',               '22.333333333333332',
        '23.1666666667',      '23.8333333333',      '23.6666666667',
        '23.6666666667',      '24.0',               '24.5',
        '24.5',               '24.6666666667',      '26.0',
        '26.5',               '27.0',               '27.1666666667',
        '27.1666666667',      '26.6666666667',
    ]
    input10 = [
        20.0, 22.0, 24.0,
        25.0, 23.0, 26.0,
        28.0, 26.0, 29.0,
        27.0, 28.0, 30.0,
        27.0, 29.0, 28.0,
    ]
    output10 = [
        '20.0',               '21.0',               '22.0',
        '22.75',              '22.8',               '23.333333333333332',
        '24.0',               '24.25',              '24.77777777777778',
        '25.0',               '25.8',               '26.6',
        '26.9',               '27.3',               '27.8',
    ]
    test_moving_average( 6, input06, output06, notify)
    test_moving_average(10, input10, output10, notify)
    print('')
