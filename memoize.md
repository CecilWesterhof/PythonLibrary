# Why can memoize be useful?

There are functions that are expensive to calculate. Especially recursive functions. When those functions are only dependent on there input values it is a good idea to cache the results after calculating them and next time return the value out of the cache.

A good example are the Fibonacci Numbers. They are defined as follows:
* F0 = 0
* F1 = 1
* Fn = Fn-1 + Fn-2

When calculated in the normal recursive way the time taken in seconds for 100 calculations is:
* F15 -> 0.04
* F20 -> 0.35
* F25 -> 3.8
* F30 -> 42
* F35 -> 482

When calculated with memoize the values become:
* F15 -> 0.0016
* F20 -> 0.0023
* F25 -> 0.0027
* F30 -> 0.0032
* F35 -> 0.0037

So instead of an exponential growth there is a linear growth. This means that even for very big values the calculation is fast:
* F310 -> 0.036
* F315 -> 0.036
* F320 -> 0.038
* F325 -> 0.038
* F330 -> 0.038
