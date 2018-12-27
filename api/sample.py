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
    
@route('/api/recon/<trade_date>')
def api_recon_get(trade_date):
    logging.debug("IN api_recon_get")
    #return "['Hello', 'World', 'tradedate']"
    data_store_filepath = "./data/json/{0}.json".format(trade_date)
    with open(data_store_filepath, "r") as infile:
        json_string = infile.read()
    data = json.loads(json_string)
    return json_string


    # with tempfile.TemporaryFile() as temp_file:
    #     # Read contents of the upload file and save dump it into temp file
    #     upload_file_content = upload_file.file.read()
    #     temp_file.write(upload_file_content)
    #     temp_file.flush()