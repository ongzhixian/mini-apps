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

########################################
# SGX pages
########################################

@route('/trading/sgx')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-page.html').render(context)


@route('/trading/sgx/charts/test')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-page.html').render(context)

@route('/trading/sgx/charts/test-line')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-line-page.html').render(context)

@route('/trading/sgx/charts/test-area')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-area-page.html').render(context)

@route('/trading/sgx/charts/test-bar')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-bar-page.html').render(context)

@route('/trading/sgx/charts/test-radar')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-radar-page.html').render(context)

@route('/trading/sgx/charts/test-doughnut')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-doughnut-page.html').render(context)

@route('/trading/sgx/charts/test-bubble')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-bubble-page.html').render(context)

@route('/trading/sgx/charts/test-scatter')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-scatter-page.html').render(context)

@route('/trading/sgx/charts/test-polar')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-polar-page.html').render(context)

@route('/trading/sgx/charts/test-mixed')
def display_trading_sgx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/sgx-charts-test-mixed-page.html').render(context)

########################################
# ASX pages
########################################

@route('/trading/asx')
def display_trading_asx_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/trading/asx-page.html').render(context)

########################################
# Ref pages
########################################

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