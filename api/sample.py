import json
import logging
import os
from helpers.page_helpers import *

################################################################################
# Setup helper functions
################################################################################

# N/A

################################################################################
# Setup routes
################################################################################

@route('/api/sample', method='POST')
def api_sample_post():
    logging.debug("IN api_sample_post")
    # json_data = request.json
    # logging.info(str(json_data))
    cwd = os.getcwd()
    logging.info(cwd)


@route('/api/sample')
def api_sample_get():
    logging.debug("IN api_sample_get")
    return "['Hello', 'World']"
    