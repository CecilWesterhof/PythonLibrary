# PythonLibrary

A Python library with useful functions.
Copyright: 2015 by Cecil Westerhof
Contact: (python@decebal.nl)

If you would like to see a certain function/class: let me know.

The files contain the following (exception) classes and functions:

In fileBasedMessages.py:
- Functions:
  - dequeue_message
  - get_message
  - get_nr_of_messages
  - queue_message
  - save_history
  - used_messages

In mathDecebal.py:
- Functions:
  - fibonacci
  - fibonacci_memoize
  - fibonacci_memoize_after_clearing
  - time_function (for testing)


In timeDecebal.py:
- Classes:
  - Timer
- Functions:
  - time_test

In twitterDecebal.py:
- Functions:
  - send_message

In utilDecebal.py:
- Exception classes:
  - SerializationError
- Classes:
  - MovingAverage
  - TimedMessage
- Functions:
  - convert_serialization
  - find
  - get_serialization
  - human_readable_size
  - memoize
  - save_serialization
  - time_fetchURLs
- Testing functions:
  - test_moving_average


There is also template.py: just a template to use when writing new modules.
