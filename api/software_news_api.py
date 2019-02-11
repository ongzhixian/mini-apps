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
    json_data = request.json
    print("IN api_software_news_post")
    print(json_data)
    rec = json_data
    sw_news_data.init()
    sw_news_data.update_software_news(
        rec['name'],
        rec['version'],
        rec['last_updated'],
        rec['md5_hash'],
        rec['last_checked']
    )

    op_result = {
        "result": "OK",
        "errors": [],
    }
    return json.dumps(op_result)
    # logging.info(str(json_data))
    # cwd = os.getcwd()
    # logging.info(cwd)

    
# @route('/api/toto/last-draw')
# def api_toto_last_draw_get():
#     logging.debug("IN api_toto_last_draw_get")
#     lot_result = toto_data.get_last_draw()
#     # ZX: lot = List of Tuple
#     return json.dumps(lot_result)


# @route('/api/toto/<draw_date>')
# def api_toto_get(draw_date):
#     logging.debug("IN api_toto_get")
#     #return "['Hello', 'World', 'tradedate']"
#     data_store_filepath = "./data/json/{0}.json".format(draw_date)
#     with open(data_store_filepath, "r") as infile:
#         json_string = infile.read()
#     data = json.loads(json_string)
#     return json_string



# @route('/api/toto/sample')
# def api_sample_get():
#     logging.debug("IN api_sample_get")
#     return "['Hello', 'World']"
    



    # with tempfile.TemporaryFile() as temp_file:
    #     # Read contents of the upload file and save dump it into temp file
    #     upload_file_content = upload_file.file.read()
    #     temp_file.write(upload_file_content)
    #     temp_file.flush()