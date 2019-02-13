import json
import logging
import os
from helpers.page_helpers import *
from modules import sw_news_data

################################################################################
# Setup helper functions
################################################################################

# N/A

################################################################################
# Setup routes
################################################################################

@route('/api/software/news', method='POST')
def api_software_news_post():
    logging.debug("IN api_software_news_post")
    logging.debug(request.json)

    # 
    sw_news_data.init()
    sw_news_data.add_news(request.json)

    result = {
        "post_data": request.json,
        "operation" : "save record",
        "result": "success"
    }
    return json.dumps(result)


# @route('/api/toto/<draw_date>')
# def api_toto_get(draw_date):
#     logging.debug("IN api_toto_get")
#     #return "['Hello', 'World', 'tradedate']"
#     data_store_filepath = "./data/json/{0}.json".format(draw_date)
#     with open(data_store_filepath, "r") as infile:
#         json_string = infile.read()
#     data = json.loads(json_string)
#     return json_string


# @route('/api/toto/sample', method='POST')
# def api_sample_post():
#     logging.debug("IN api_sample_post")
#     # json_data = request.json
#     # logging.info(str(json_data))
#     cwd = os.getcwd()
#     logging.info(cwd)

