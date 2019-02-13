################################################################################
# Import statements
################################################################################

import logging
import os
import time
import uuid
import bottle
import json

from datetime import datetime, timedelta

from bottle import default_app, run, route, request, response, redirect, abort, error
from .app_helpers import appconfig

from modules import cryptograph

################################################################################
# Function decorators
################################################################################

def get_session_store_path():
    sess_cookie_name = str(appconfig['application']["sess_cookie_name"])
    # If cookie is NOT in request, generate cookie
    if sess_cookie_name not in bottle.request.cookies:
        print("In cookie not exists")
        sess_cookie_value = add_sess_cookie(sess_cookie_name)
    else: # cookie exists;
        print("In cookie exists")
        sess_cookie_value = bottle.request.cookies[sess_cookie_name]
    session_store_path = "./data/sessions/{0}".format(sess_cookie_value)
    return session_store_path


def require_authentication(fn):
    logging.debug("IN require_authentication(%s)" % str(fn))
    def wrapper(*args, **kwargs):
        # print 'function %s called with positional args %s and keyword args %s' % (fn.__name__, args, kwargs)
        auth_cookie_id = request.cookies.get('appconfig["application"][auth_cookie_name]')
        if not auth_cookie_id:
            logging.debug("IN auth cookie not exists")
            # redirect("/login")
            return fn(*args, **kwargs)
        else:
            logging.debug("IN auth cookie exists")
            return fn(*args, **kwargs)
    return wrapper

# def xwrapper(extra_greeting, greet2):
#     def my_decorator(func):
#         def add_to_greet():
#             func()
#             print(extra_greeting)
#         return add_to_greet
#     return my_decorator

# ZX:   To make a decorator take in arguments,
#       we wrap another decorator over a decorator
def require_auth_cookie(cookie_name, login_url):
    def fn_decorator(fn):
        def fn_logic(*args, **kwargs):
            auth_cookie_id = request.cookies.get(cookie_name)
            if not auth_cookie_id:  # auth cookie does NOT exists
                redirect(login_url)
            else: # auth cookie EXISTS
                return fn(*args, **kwargs)
        return fn_logic
    return fn_decorator


# ZX:   To make a decorator take in arguments,
#       we wrap another decorator over a decorator
def require_permission(cookie_name, permission_list, login_url):
    def fn_decorator(fn):
        def fn_logic(*args, **kwargs):
            cookie_value = request.cookies.get(cookie_name)
            print("In require_permission")
            if not cookie_value:  # cookie does NOT exists
                redirect(login_url)
            else: # cookie EXISTS
                print(cookie_value)

                # Get cryptography-keys to decrypt session
                session_store_path = get_session_store_path()
                dir_exists = os.path.isdir(session_store_path)
                if not dir_exists:
                    # Invalid session; do nothing
                    print("NO PERMISSION")
                    abort(403)
                # Else dir exists, retrieve cryptography-keys
                file_path = os.path.join(session_store_path, "cryptography-keys.json")
                with open(file_path, "r+b") as f:
                    aes_crypto_json = f.read()
                    print(aes_crypto_json)
                    aes_crypto = json.loads(aes_crypto_json)

                    # Use aes_crypto to decrypt
                    # aes_key = cryptograph.hex_string_to_byte_string(aes_crypto['key'])
                    # aes_iv  = cryptograph.hex_string_to_byte_string(aes_crypto['iv'])
                    # encrypted_cookie_value = cryptograph.aes_encrypt_as_hex(aes_key, aes_iv, cookie_value)
                    # encrypted_cookie_value = cryptograph.aes_encrypt_as_hex(aes_crypto, cookie_value)
                    # import binascii
                    # encrypted_cookie_value_hex = binascii.hexlify(encrypted_cookie_value)

                    plain_text = cryptograph.aes_decrypt_from_hex(aes_crypto, cookie_value)
                    print(plain_text)

                    cookie_val_list = plain_text.split("|")
                    # cookie_val_list should at least be 2 elements long
                    # cookie_val_list composed  of:
                    # 1.    email/username
                    # 2.    roles
                    if len(cookie_val_list) < 2:
                        print("INVALID.")
                        abort(403)
                    role_list = cookie_val_list[1].split(",")
                    print(role_list)
                    if set(role_list) & set(permission_list):
                        print("VALID PERMISSION")
                    else:
                        print("INVALID PERMISSION")
                        abort(403)
                return fn(*args, **kwargs)
        return fn_logic
    return fn_decorator


################################################################################
# Basic functions
################################################################################

########################################
# Define application hooks
########################################

##########
# auth_cookie

def add_auth_cookie(cookie_name, cookie_value):
    # Using UUID4 to generate cookie value
    new_uuid = uuid.uuid4()
    new_uuid_hex = new_uuid.hex
    # Set expiry to be a year (366 days) from now.
    expiry = ((datetime.utcnow() + timedelta(366)) - datetime(1970, 1, 1)).total_seconds()
    #bottle.response.set_cookie(cookie_name, new_uuid.hex, httponly=True, expires=expiry)

    # sess_cookie_name = str(appconfig['application']["sess_cookie_name"])

    # # If cookie is NOT in request, generate cookie
    # if sess_cookie_name not in bottle.request.cookies:
    #     print("In cookie not exists")
    #     sess_cookie_value = add_sess_cookie(sess_cookie_name)
    # else: # cookie exists;
    #     print("In cookie exists")
    #     sess_cookie_value = bottle.request.cookies[sess_cookie_name]

    # session_store_path = "./data/sessions/{0}".format(sess_cookie_value)

    session_store_path = get_session_store_path()
    dir_exists = os.path.isdir(session_store_path)
    if not dir_exists:
        # Invalid session; do nothing
        return
    # Else dir exists, retrieve cryptography-keys
    file_path = os.path.join(session_store_path, "cryptography-keys.json")
    with open(file_path, "r+b") as f:
        aes_crypto_json = f.read()
        print(aes_crypto_json)
        aes_crypto = json.loads(aes_crypto_json)

        # aes_key = cryptograph.hex_string_to_byte_string(aes_crypto['key'])
        # aes_iv  = cryptograph.hex_string_to_byte_string(aes_crypto['iv'])
        # encrypted_cookie_value = cryptograph.aes_encrypt(aes_key, aes_iv, cookie_value)
        # import binascii
        # encrypted_cookie_value_hex = binascii.hexlify(encrypted_cookie_value)

        # Use aes_crypto to encrypt
        encrypted_cookie_value_hex = cryptograph.aes_encrypt_as_hex(aes_crypto, cookie_value)
    bottle.response.set_cookie(cookie_name, encrypted_cookie_value_hex, path='/', httponly=True, expires=expiry)
    return new_uuid_hex

# ZX:   Not used; auth cookie should not be hooked
#       This was an error in coding; what we really want to hook is session cookie
#       This is done below.
def add_auth_cookie_hook():
    """Add auth cookie if user does not have auth cookie"""
    # Name of the cookie that we want to check for
    auth_cookie_name = str(appconfig['application']["auth_cookie_name"])
    # If cookie is NOT in request, generate cookie
    if auth_cookie_name not in bottle.request.cookies:
        add_auth_cookie(auth_cookie_name)
        # # Using UUID4 to generate cookie value
        # new_uuid = uuid.uuid4()
        # new_uuid_hex = new_uuid.hex
        # # Set expiry to be a year (366 days) from now.
        # expiry = ((datetime.utcnow() + timedelta(366)) - datetime(1970, 1, 1)).total_seconds()
        # bottle.response.set_cookie(auth_cookie_name, new_uuid.hex, httponly=True, expires=expiry)
        # # Create a session folder
        
        # session_store_path = "./data/sessions/{0}".format(new_uuid_hex)
        # dir_exists = os.path.isdir(session_store_path)
        # if not dir_exists:
        #     os.mkdir(session_store_path)

##########
# sess_cookie
def delete_sess_cookie(res):
    sess_cookie_name = str(appconfig['application']["sess_cookie_name"])
    print(res)
    #res.set_cookie(sess_cookie_name, value='', path='/zx/', httponly=True, expires=0)
    res.delete_cookie(sess_cookie_name, path='/zx/')
    # bottle.response.delete_cookie(sess_cookie_name)

def add_sess_cookie(cookie_name):
    # Using UUID4 to generate cookie value
    new_uuid = uuid.uuid4()
    new_uuid_hex = new_uuid.hex
    # Set expiry to be a year (366 days) from now.
    expiry = ((datetime.utcnow() + timedelta(366)) - datetime(1970, 1, 1)).total_seconds()
    bottle.response.set_cookie(cookie_name, new_uuid.hex, path='/', httponly=True, expires=expiry)
    # ZX:   Bottle does not have a facility for tracking session
    #       We use the filesystem with each folder representing a singular session. 
    # Create a session folder
    session_store_path = "./data/sessions/{0}".format(new_uuid_hex)
    dir_exists = os.path.isdir(session_store_path)
    if not dir_exists:
        os.mkdir(session_store_path)
        file_path = os.path.join(session_store_path, "cryptography-keys.json")
        aes_crypto =  cryptograph.make_keys("AES", 32, 16)
        with open(file_path, "w+b") as f:
            f.write(json.dumps(aes_crypto))
    return new_uuid_hex

def add_sess_cookie_hook():
    """Add session cookie if user does not have session cookie"""
    # Name of the cookie that we want to check for
    sess_cookie_name = str(appconfig['application']["sess_cookie_name"])
    # If cookie is NOT in request, generate cookie
    if sess_cookie_name not in bottle.request.cookies:
        add_sess_cookie(sess_cookie_name)
        

########################################
# Define error pages
########################################

@error(403)
def error403(error):
    bottle.response.set_cookie('mini-apps-session', '', path='/', expires=0)
    bottle.response.set_cookie('ZX_AUTH', '', path='/', expires=0)
    return '403 - Forbidden'

@error(404)
def error404(error):
    #bottle.response.set_cookie('mini-apps-session', '', expires=0)
    bottle.response.set_cookie('mini-apps-session', '', path='/',expires=0)
    bottle.response.set_cookie('ZX_AUTH', '', path='/', expires=0)
    return 'Nothing here, sorry'

@error(500)
def error500(error):
    #bottle.response.set_cookie('mini-apps-session', '', expires=0)
    return error



########################################
# Define core functions
########################################

def get_app():
    app = default_app()

    # add application hooks here
    # TODO: Add setup for add_auth_cookie_hook; it needs a sessions folder in data folder
    #app.add_hook('after_request', add_auth_cookie_hook)
    app.add_hook('after_request', add_sess_cookie_hook)
    return app

def get_default_context(request):
    context = {
        'auth_cookie'       : request.cookies.get(appconfig["application"]["auth_cookie_name"]),
        'current_datetime'  : datetime.now()
    }
    return context


################################################################################
# Variables dependent on Application basic functions
################################################################################

# N/A

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    pass
