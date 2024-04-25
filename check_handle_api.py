#!/usr/bin/env python3

# Kyriakos Gkinis <kyrginis@admin.grnet.gr>, 2017

import argparse
import logging
import sys
import signal
import time
import traceback

from requests.exceptions import SSLError
from requests.packages.urllib3 import disable_warnings

from pyhandle.clientcredentials import PIDClientCredentials
from pyhandle.handleclient import PyHandleClient
import pyhandle.handleexceptions as hdlex


TEST_SUFFIX='NAGIOS-' +  time.strftime("%Y%m%d-%H%M%S",time.gmtime())
VALUE_ORIG='http://www.' + TEST_SUFFIX + '.com/1'
VALUE_AFTER='http://www.' + TEST_SUFFIX + '.com/2'

def handler(signum, stack):
    print("UNKNOWN: Timeout reached, exiting.")
    sys.exit(3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EPIC API create, read, update, delete probe')
    req = parser.add_argument_group('required arguments')
    req.add_argument('-f', '--file', action='store', dest='json_file', required=True,
            help='JSON credentials file')
    req.add_argument('-p', '--prefix', action='store', dest='prefix',
            help='prefix to test')
    req.add_argument('-t', '--timeout', action='store', dest='timeout',
            help='timeout')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug',
            help='debug mode')

    param = parser.parse_args()

    if param.timeout and int(param.timeout) > 0 :
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(int(param.timeout))

    if param.debug:
        logging.basicConfig(level=logging.DEBUG)

    try:

        print("Creating credentials")
        cred = PIDClientCredentials.load_from_JSON(param.json_file)
        client = PyHandleClient("rest").instantiate_with_credentials(cred)

        all_creds = cred.get_all_args()

        # If not in debug mode, disable InsecureRequestWarnings when "HTTPS_verify": "False"
        if (not param.debug and 'HTTPS_verify' in all_creds
                and all_creds['HTTPS_verify'].lower()=='false'):
            disable_warnings() 

        print('PID prefix ' + cred.get_prefix())
        print('Server ' + cred.get_server_URL())

        handle = cred.get_prefix() + '/' + TEST_SUFFIX
        
        # Create test
        print("Creating handle " + handle)
        create_result = client.register_handle(
            handle, VALUE_ORIG)

        if create_result == handle:
            print("OK: Create handle successful.")
        else:
            print("CRITICAL: Create handle returned unexpected response.")
            sys.exit(2)
         
        # Read test
        key = 'URL'
        read_value = client.get_value_from_handle(
            handle, key)
        
        if param.debug:
            print("DEBUG:Handle value after Create operation: " + read_value)

        if read_value == VALUE_ORIG:
            print("OK: Read handle successful.")
        else:
            print("CRITICAL: Read handle returned unexpected response.")
            client.delete_handle(handle)
            sys.exit(2)
        
        # Modify test
        client.modify_handle_value(
            handle, **{key: VALUE_AFTER} )

        get_value_result = client.get_value_from_handle(
            handle, key)

        if param.debug:
            print("DEBUG:Handle value after Modify operation: " + get_value_result)

        if get_value_result == VALUE_AFTER:
            print("OK: Modify handle successful.")
        else:
            print("CRITICAL: Modify handle value returned unexpected value.")
            print("Expected : " + VALUE_AFTER)
            print("Returned : " + get_value_result)
            client.delete_handle(handle)
            sys.exit(2)
        
        # Delete test

        delete_result = client.delete_handle(handle)
        print("OK: Delete handle successful.")
        
    except (hdlex.GenericHandleError, hdlex.CredentialsFormatError, hdlex.HandleAlreadyExistsException,
                hdlex.HandleSyntaxError, hdlex.HandleNotFoundException, hdlex.HandleAuthenticationError,
                SSLError) as e:
        if param.debug :
            print("CRITICAL: " + traceback.format_exc())
        else :
            print("CRITICAL: " + str(e))
        sys.exit(2)
    except Exception as e:
        if param.debug :
            print("UNKNOWN: " + traceback.format_exc())
        else:
            print("UNKNOWN: " + str(e))
        sys.exit(3)
    

