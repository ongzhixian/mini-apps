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

@route('/url_dump')
def display_home_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/url_dump/home-page.html').render(context)