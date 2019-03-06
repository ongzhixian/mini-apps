import json
import logging
import os
from helpers.page_helpers import *
# from modules import toto_data
# from modules import game_trading


################################################################################
# What is this API suppose to start
################################################################################
# /api/game/trading/<verb>-<noun>
# /api/game/trading/new-game    - Starts new simulation; returns session id
# /api/game/trading/get-info    - Get various info given session id and parameters
# /api/game/trading/get-price   - Get price data for given day


# /api/game/trading/add-player  - Register participant to session

################################################################################
# Setup helper functions
################################################################################

# N/A

################################################################################
# Setup routes
################################################################################

# @route('/api/game/trading/new-game')
def api_game_trading_new_game():
    logging.debug("IN api_game_trading_new_game")
    
    game_session = {
        "session_id"        : "yyyyMMdd",
        "start_trade_date"  : "yyyyMMdd"
    }
    #game_trading.new_session()
    lot_result = toto_data.get_last_draw()
    # ZX: lot = List of Tuple
    return json.dumps(game_session)


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

# # @route('/api/toto/sample', method='POST')
# # def api_sample_post():
# #     logging.debug("IN api_sample_post")
# #     # json_data = request.json
# #     # logging.info(str(json_data))
# #     cwd = os.getcwd()
# #     logging.info(cwd)


# # @route('/api/toto/sample')
# # def api_sample_get():
# #     logging.debug("IN api_sample_get")
# #     return "['Hello', 'World']"
    



#     # with tempfile.TemporaryFile() as temp_file:
#     #     # Read contents of the upload file and save dump it into temp file
#     #     upload_file_content = upload_file.file.read()
#     #     temp_file.write(upload_file_content)
#     #     temp_file.flush()