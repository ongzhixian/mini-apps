################################################################################
# Modules and functions import statements
################################################################################

import logging
import pdb
from helpers.app_helpers import *
from helpers.page_helpers import *
from helpers.jinja2_helpers import *

################################################################################
# Setup helper functions
################################################################################

# N/A
def is_authenticate_credentials(email, password):
    return True

################################################################################
# Setup commonly used routes
################################################################################

@route('/zx/login', method=['POST','GET'])
def display_zx_login_page(errorMessages=None):
    context = get_default_context(request)
    logging.debug(context['auth_cookie'])
    logging.debug(context['current_datetime'])

    if request.method == 'POST':
        pass
        logging.debug("In POST")
        # Do form processing here
        if 'email_input' in request.forms.keys():
            email_input = request.forms['email_input']
        if 'password_input' in request.forms.keys():
            password_input = request.forms['password_input']
        if is_authenticate_credentials(email_input, password_input):
            redirect("/zx")
        else:
            context["error_message"] = "Invalid credentials."
    return jinja2_env.get_template('html/zx/login-page.html').render(context)


@route('/zx')
def display_home_page(errorMessages=None):
    context = get_default_context(request)
    #response.set_cookie('username', 'the username')
    logging.debug(context['auth_cookie'])
    logging.debug(context['current_datetime'])
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

# @route('/test1')
# @route('/test1/')
# def display_test_page(errorMessages=None):
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/site/test1-page.html').render(context)

# @route('/test2')
# def display_test2_page(errorMessages=None):
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/site/test2-page.html').render(context)

# @route('/test3')
# def display_test3_page(errorMessages=None):
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/site/test3-page.html').render(context)

# @route('/test4')
# def display_test4_page(errorMessages=None):
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/site/test4-page.html').render(context)
