"""Some utilty functions that could be handy"""

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
