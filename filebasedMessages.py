"""
Some functions for file based message handling
It does not take care of race conditions
So if mutating functions are called at the same time from different
threads/programs corruption is possible.

Defined functions:
- dequeue_message
- get_indexed_message
- get_nr_of_messages
- get_random_message
- queue_message
- save_history
- used_messages
"""

from itertools  import islice
from marshal    import dump, load
from os         import rename
from os.path    import expanduser, split
from random     import randint
from tempfile   import NamedTemporaryFile


class GetMessageError(Exception):
    pass


def dequeue_message(message_filename, save_filename = None, isLarge = False):
    """
    Get the first message from a file and remove it from the file
    If save_filename not None it is used to save the message
    Use isLarge = True when you do not want to load the file in memory
    """

    real_file = expanduser(message_filename)
    if get_nr_of_messages(real_file) == 0:
        raise GetMessageError('{0} does not contains any messages'.
                              format(message_filename))
    if not isLarge:
        with open(real_file, 'r') as f:
            messages = f.readlines()
        message = messages.pop(0).rstrip()
        with open(expanduser(message_filename), 'w') as f:
            f.writelines(messages)
    else:
        (filepath,
         filename)  = split(real_file)[0]
        message     = get_indexed_message(real_file, 0)
        with NamedTemporaryFile(mode = 'w', prefix = filename + '_',
                                dir = filepath, delete = False) as tf:
            tempfile = tf.name
            with open(real_file, 'r') as f:
                for line in islice(f, 1, None):
                    tf.write(line)
        rename(tempfile, real_file)
    if save_filename != None:
        queue_message(save_filename, message)
    return message

def get_indexed_message(message_filename, index):
    """
    Get index message from a file, where 0 gets the first message
    A negative index gets messages indexed from the end of the file
    Use get_nr_of_messages to get the number of messages in the file
    """

    return get_message_slice(message_filename, index, index)[0]

def get_message_slice(message_filename, start, end, skip = 0):
    """
    Get a slice of messages, where 0 is the first message
    Works with negative indexes
    The values can be ascending and descending
    Skip needs to be greater or equal 0
    """

    message_list    = []
    real_file       = expanduser(message_filename)
    nr_of_messages  = get_nr_of_messages(real_file)
    if start < 0:
        start += nr_of_messages
    if end < 0:
        end += nr_of_messages
    assert((start >= 0) and (start < nr_of_messages))
    assert((end   >= 0) and (end   < nr_of_messages))
    assert  skip  >= 0, 'Step needs to be positve'
    if start > end:
        tmp             = start
        start           = end
        end             = tmp
        need_reverse    = True
    else:
        need_reverse    = False
    with open(real_file, 'r') as f:
        for message in islice(f, start, end, skip + 1):
            message_list.append(message.rstrip())
    if need_reverse:
        message_list.reverse()
    return message_list

def get_nr_of_messages(message_filename):
    i = -1
    with open(expanduser(message_filename), 'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def get_random_message(message_filename, marshal_filename,
                history, need_warning, max_tries):
    """
    Get a random message from a file which is not used in 'recent history'
    """

    not_list    = used_messages(marshal_filename)
    nr_of_msg   = get_nr_of_messages(message_filename)
    tries       = 0

    # If there are not more messages as history you will run out of messages
    if nr_of_msg <= history:
        print('History is to long. History: {0}. Nr of messages: {1}.'.
            format(history, nr_of_msg))
    # With at least 2 times as much messages as history
    # a new message is easily generated
    elif nr_of_msg < (2 * history):
        print('History is quite long. History: {0}. Nr of messages: {1}.'.
            format(history, nr_of_msg))
    # Need a do ... while loop
    while True:
        index   = randint(0, nr_of_msg - 1)
        tries  += 1
        if not index in not_list:
            break
        if tries >= max_tries:
            raise GetMessageError('Did not get a message after {0} tries'.
                                  format(tries))
    print('Used {0} tries to get a message'.format(tries)) ### Temporaly
    if tries >= need_warning:
        print('Needed {0} tries to get a message'.format(tries))
    # Add last used to list
    not_list.append(index)
    # Remove first of list if longer as history
    if len(not_list) > history:
        del not_list[0]
    save_history(marshal_filename, not_list)
    return get_indexed_message(message_filename, index)

def queue_message(message_filename, message):
    """Append a message to a file"""

    with open(expanduser(message_filename), 'a') as f:
        f.write(message + '\n')

def save_history(marshal_filename, list_to_save):
    """Save message history"""

    with open(expanduser(marshal_filename), 'w') as f:
        dump(list_to_save, f)

def used_messages(marshal_filename):
    """Get message history"""

    with open(expanduser(marshal_filename), 'r') as f:
        return load(f)
