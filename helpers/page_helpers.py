################################################################################
# Import statements
################################################################################

import logging
import os
import time
import uuid
import bottle
import page_helpers

from datetime import datetime, timedelta

from bottle import default_app, run, route, request, response, redirect, abort
from app_helpers import appconfig

################################################################################
# Function decorators
################################################################################

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

################################################################################
# Basic functions
################################################################################

########################################
# Define application hooks
########################################

def add_auth_cookie(cookie_name):
    # Using UUID4 to generate cookie value
    new_uuid = uuid.uuid4()
    new_uuid_hex = new_uuid.hex
    # Set expiry to be a year (366 days) from now.
    expiry = ((datetime.utcnow() + timedelta(366)) - datetime(1970, 1, 1)).total_seconds()
    bottle.response.set_cookie(cookie_name, new_uuid.hex, httponly=True, expires=expiry)
    # Create a session folder
    
    session_store_path = "./data/sessions/{0}".format(new_uuid_hex)
    dir_exists = os.path.isdir(session_store_path)
    if not dir_exists:
        os.mkdir(session_store_path)
    return new_uuid_hex

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


########################################
# Define core functions
########################################

def get_app():
    app = page_helpers.default_app()

    # add application hooks here
    # TODO: Add setup for add_auth_cookie_hook; it needs a sessions folder in data folder
    app.add_hook('after_request', add_auth_cookie_hook)
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