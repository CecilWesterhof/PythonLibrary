from __future__ import print_function

import gc
import timeit


##### Classes

# The code for the class Timer is mostly from Steven D'Aprano:
# http://code.activestate.com/recipes/577896-benchmark-code-with-the-with-statement/
# I did some cosmetic changes.
# The documentation is mine.
class Timer:
    '''
    Class to easily time things.
    Use only for things that take at least several seconds.

    Example usage:
    t = Timer()
    with t:
        <CODE TO TIME>
    used_time   = t.interval
    '''

    def __enter__(self):
        if self.disable_gc:
            self.gc_state = gc.isenabled()
            gc.disable()
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        self.end        = self.timer()
        if self.disable_gc and self.gc_state:
            gc.enable()
        self.interval   = self.end - self.start
        if self.verbose:
            print('Time taken: %f seconds' % self.interval)

    def __init__(self, timer = None, disable_gc = False, verbose = False):
        if timer is None:
            timer       = timeit.default_timer
        self.disable_gc = disable_gc
        self.start      = self.end = self.interval = None
        self.timer      = timer
        self.verbose    = verbose


##### Functions

def time_test(function, arguments, print_time = True):
    '''
    Sometimes you want the time used of a function AND the output of the function.
    Default this function prints the time and returns the result.
    Arguments: function, tuple with the arguments for the function and
    optional print_time.
    Setting print_time to False will return used_time and result as a tuple.
    '''

    t = Timer()
    with t:
        results = function(*arguments)
    used_time   = t.interval
    if print_time:
        print('It took {0} seconds'.format(used_time))
    else:
        results = (used_time, results)
    return results
