'''
Some functions for using Twitter with libturpial.

When you like something to be implemented let me know:
    python@decebal.nl

Defined functions:
- send_message
'''

from __future__ import print_function

import certifi
import sys
import time
import urllib3
import urllib3.contrib.pyopenssl


from libturpial.api.core    import Core
from libturpial.exceptions  import ServiceOverCapacity

urllib3.contrib.pyopenssl.inject_into_urllib3()
http = urllib3.PoolManager(
    cert_reqs   = 'CERT_REQUIRED', # Force certificate check.
    ca_certs    = certifi.where(), # Path to the Certifi bundle.
)

def send_message(
        account_id, message, max_tries, give_error,
        wait_time = 60, notify = True):
    error_msg   = 'Something went wrong with: ' + message
    tries       = 0
    while True:
        try:
            Core().update_status(account_id, message)
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
