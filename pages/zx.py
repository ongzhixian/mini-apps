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

@route('/zx')
def display_home_page(errorMessages=None):
    context = get_default_context(request)
    #response.set_cookie('username', 'the username')
    return jinja2_env.get_template('html/zx/home-page.html').render(context)

# @route('/about')
# def display_about_page(errorMessages=None):
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/site/about-page.html').render(context)

# @route('/contact')
# def display_contact_page(errorMessages=None):
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/site/contact-page.html').render(context)

# @route('/toto')
# def display_test_page(errorMessages=None):
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/site/toto-page.html').render(context)

########################################
# Other test routes
########################################

@route('/test1')
@route('/test1/')
def display_test_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/test1-page.html').render(context)

@route('/test2')
def display_test2_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/test2-page.html').render(context)

@route('/test3')
def display_test3_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/test3-page.html').render(context)

@route('/test4')
def display_test4_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/test4-page.html').render(context)
