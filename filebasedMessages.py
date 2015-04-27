"""
Some functions for file based message habdling
It does not take care of race conditions
So if it is called at the same time from different threads/programs
corruption is possible.
Defined functions:
- dequeue_message
- get_message
- get_nr_of_messages
- queue_message
- save_history
- used_messages
"""

from marshal    import dump, load
from os.path    import expanduser
from random     import randint


class GetMessageError(Exception):
    pass


def dequeue_message(message_filename, save_filename = None):
    """
    Get the first message from a file and remove it from the file
    If save_filename not None use it to save the message
    """

    messages    = open(expanduser(message_filename), 'r').readlines()
    nr_of_msg   = len(messages)

    if nr_of_msg == 0:
        raise GetMessageError, \
            '{0} does not contains any messages'.format(message_filename)
    message = messages.pop(0).rstrip()
    open(expanduser(message_filename), 'w').writelines(messages)
    if save_filename != None:
        queue_message(save_filename, message)
    return message

def get_message(message_filename, marshal_filename,
                history, need_warning, max_tries):
    """
    Get a random message from a file which is not used in 'recent history'
    """

    messages    = open(expanduser(message_filename), 'r').readlines()
    not_list    = used_messages(marshal_filename)
    nr_of_msg   = len(messages)
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
        index = randint(0, nr_of_msg - 1)
        ++tries
        if not index in not_list:
            break
        if tries >= max_tries:
            raise GetMessageError, 'Did not get a message after {0} tries'. \
                format(tries)
    if tries >= need_warning:
        print('Needed {0} tries to get a message'.format(tries))
    # Add last used to list
    not_list.append(index)
    # Remove first of list if longer as history
    if len(not_list) > history:
        del not_list[0]
    save_history(marshal_filename, not_list)
    return messages[index].rstrip()

def get_nr_of_messages(message_filename):
    return len(open(expanduser(message_filename), 'r').readlines())

def queue_message(message_filename, message):
    """Append a message to a file"""

    open(expanduser(message_filename), 'a').write(message + '\n')

def save_history(marshal_filename, list_to_save):
    """Save message history"""

    marshal_file = open(expanduser(marshal_filename), 'w')
    dump(list_to_save, marshal_file)
    marshal_file.close()

def used_messages(marshal_filename):
    """Get message history"""

    marshal_file    = open(expanduser(marshal_filename), 'r')
    not_list        = load(marshal_file)
    marshal_file.close()
    return not_list
