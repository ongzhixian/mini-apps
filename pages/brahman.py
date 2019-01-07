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

@route('/brahman/')
@route('/brahman')
def display_home_page(errorMessages=None):
    context = get_default_context(request)
    response.set_cookie('username', 'the username')
    return jinja2_env.get_template('html/brahman/home-page.html').render(context)

@route('/brahman/reconciliation/test1')
def display_test_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/brahman/test1-page.html').render(context)

@route('/brahman/reconciliation/test2')
def display_test2_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/brahman/test2-page.html').render(context)

# @route('/brahman/reconciliation/test3')
# def display_test3_page(errorMessages=None):
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/brahman/test3-page.html').render(context)
