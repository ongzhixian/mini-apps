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

@route('/favicon.ico')
def get_favicon():
    return bottle.static_file('favicon.ico', root='./')

@route('/<filename:path>')  
def static(filename):  
    '''  
    Serve static files
    '''  
    return bottle.static_file(filename, root='./static')

@route('/')
def display_home_page(errorMessages=None):
    context = get_default_context(request)
    response.set_cookie('username', 'the username')
    return jinja2_env.get_template('html/site/home-page.html').render(context)

@route('/about')
def display_about_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/about-page.html').render(context)

@route('/contact')
def display_contact_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/contact-page.html').render(context)

@route('/test')
def display_test_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/test-page.html').render(context)

@route('/test2')
def display_test2_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/test2-page.html').render(context)

@route('/test3')
def display_test3_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/site/test3-page.html').render(context)
