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

@route('/software/')
@route('/software')
def display_software_home_page(errorMessages=None):
    redirect("/software/news")
    context = get_default_context(request)
    response.set_cookie('username', 'the username')
    return jinja2_env.get_template('html/software/home-page.html').render(context)
    

@route('/software/news')
def display_software_news_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/software/news-page.html').render(context)
