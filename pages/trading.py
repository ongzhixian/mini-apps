################################################################################
# Modules and functions import statements
################################################################################

import pdb
from helpers.app_helpers import *
from helpers.page_helpers import *
from helpers.jinja2_helpers import *

################################################################################
# Setup helper functions
################################################################################

# N/A

################################################################################
# Setup commonly used routes
################################################################################


@route('/trading/')
@route('/trading')
def display_trading_home_page(errorMessages=None):
    context = get_default_context(request)
    #response.set_cookie('username', 'the username')
    return jinja2_env.get_template('html/trading/home-page.html').render(context)

@route('/trading/sgx')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-page.html').render(context)

@route('/trading/asx')
def display_trading_asx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/asx-page.html').render(context)


@route('/trading/ref')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/ref-page.html').render(context)

@route('/trading/ref/futures/month-codes')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/ref-futures-month-code-page.html').render(context)

@route('/trading/ref/options/month-codes')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/ref-options-month-code-page.html').render(context)