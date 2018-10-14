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

################################################################################
# Setup commonly used routes
################################################################################

@route('/url_dump')
def display_home_page(errorMessages=None):
    context = get_default_context(request)
    return jinja2_env.get_template('html/url_dump/home-page.html').render(context)

@route('/url_dump/upload', method=['POST','GET'])
def upload_url_list(errorMessages=None):
    logging.debug("IN upload_url_list")

    if request.method == 'POST':
        logging.debug("IN POST block")
        if 'upload_file' in request.files:
            logging.debug("[upload_file] key exists in request.files")
            upload_file = request.files['upload_file']
            logging.debug(str(dir(upload_file)))
            upload_file.save("./data/" + upload_file.filename)
            logging.debug("Saving [upload_file]")
            #return 'file uploaded successfully'
    
    
    context = get_default_context(request)
    return jinja2_env.get_template('html/url_dump/home-page.html').render(context)