# This Python file uses the following encoding: utf-8

'''
Some functions for using Twitter with libturpial.

When you like something to be implemented let me know:
    python@decebal.nl

Defined functions:
- init
- send_message

Because you sometimes get a ServiceOverCapacity exception both functions
retry it max_tries when this exception occurs.
'''


# We write our code for Python3, but want it to work with Python2 also
from __future__ import print_function

# imports
import certifi
import sys
import time
import urllib3
import urllib3.contrib.pyopenssl


# froms
from libturpial.api.core    import Core
from libturpial.exceptions  import ServiceOverCapacity


class InitAlreadyDoneError(Exception):
    pass


##### Functions
def init(max_tries = 5, wait_time = 60, reinit_allowed = False):
    global _core

    if (_core != None) and not reinit_allowed:
        raise InitAlreadyDoneError
    tries = 0
    while True:
        try:
            _core = Core()
            break
        except ServiceOverCapacity:
            tries += 1
            sys.stderr.write('Tried to init _core it {0} times\n'.format(tries))
            sys.stderr.flush()
            if tries >= max_tries:
                raise
            time.sleep(wait_time)

def send_message(
        account_id, message, max_tries, give_error,
        wait_time = 60, notify = True, in_reply_id = None):
    error_msg   = 'Something went wrong with: ' + message
    tries       = 0
    while True:
        try:
            message_status = _core.update_status(account_id, message, in_reply_id)
            break
        except ServiceOverCapacity:
            tries += 1
            if notify:
                sys.stderr.write('Tried to send it {0} times\n'.format(tries))
                sys.stderr.flush()
            if tries >= max_tries:
                give_error(error_msg)
                return
            time.sleep(wait_time)
        except:
            give_error(error_msg)
            return
    return message_status.id_


##### Init

# variables
_core = None

# code
urllib3.contrib.pyopenssl.inject_into_urllib3()
http = urllib3.PoolManager(
    cert_reqs   = 'CERT_REQUIRED', # Force certificate check.
    ca_certs    = certifi.where(), # Path to the Certifi bundle.
)
