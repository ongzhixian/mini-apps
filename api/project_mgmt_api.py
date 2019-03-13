import json
import logging
import os
from helpers.page_helpers import *
from modules import project_mgmt
import sqlite3
# from modules import game_trading
from bottle import response


################################################################################
# What is this API suppose to start
################################################################################

# /api/<noun>/<verb>
# /api/<noun>/<verb>-<noun>

# /api/project/list         -
# /api/project/add          -
# /api/project/edit         -
# /api/project/delete       -

# /api/project/task/list    -
# /api/project/task/add     -
# /api/project/task/edit    -
# /api/project/task/delete  -

# /api/project/tag/list     -
# /api/project/tag/add      -
# /api/project/tag/edit     -
# /api/project/tag/delete   -



################################################################################
# Setup helper functions
################################################################################

# N/A

################################################################################
# Setup routes
################################################################################

########################################
# Get lookup lists
########################################

@route('/api/project/get_category_list')
def api_project_get_category_list():
    logging.debug("IN api_project_get_category_list")
    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        result = project_mgmt.get_lookup(cursor, 'project_category')
    # response.content_type = 'text/text; charset=UTF8' 
    # response.headers['Content-Type'] = 'application/json'
    # response.headers['Cache-Control'] = 'no-cache'
    response.content_type = 'application/json'
    return json.dumps(result)


@route('/api/project/get_status_list')
def api_project_get_status_list():
    logging.debug("IN api_project_get_status_list")
    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        result = project_mgmt.get_lookup(cursor, 'project_status')
    response.content_type = 'application/json'
    return json.dumps(result)


# A more generic api call to get lookup table list
@route('/api/project/get_lookup_list/<table_name>')
def api_project_get_lookup_list(table_name):
    logging.debug("IN api_project_get_lookup_list")
    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        result = project_mgmt.get_lookup(cursor, table_name)
    response.content_type = 'application/json'
    return json.dumps(result)

########################################
# Project related API calls
########################################

# /api/project/add          -
# /api/project/edit         -
# /api/project/delete       -

@route('/api/project/list')
def api_project_list_get():
    logging.debug("IN api_project_list_get")
    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        result = project_mgmt.get_project_list(cursor)
    response.content_type = 'application/json'
    return json.dumps(result)

@route('/api/project/add', method=["POST"])
def api_project_add():
    logging.debug("IN api_project_add")
    
    if request.content_type != "application/json":
        return

    json = request.json
    # Validate input data
    # Add record to database
    # import pdb
    # pdb.set_trace()
    project_name = json['project_name']
    project_category = json['project_category']
    project_status = json['project_status']
    timestamp = datetime.utcnow()

    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        #result = project_mgmt.get_project_list(cursor)
        records_affected = project_mgmt.upsert_project(
            cursor,
            project_name,
            project_category,
            project_status,
            timestamp
        )
    response.content_type = 'application/json'
    
    return json.dumps({
        "operation" : "api_project_add"
        "records_affected": records_affected
    })


@route('/api/project/edit', method=["POST"])
def api_project_edit_post():
    logging.debug("IN api_project_list_get")
    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        result = project_mgmt.get_project_list(cursor)
    response.content_type = 'application/json'
    return json.dumps(result)


@route('/api/project/delete', method=["POST"])
def api_project_delete_post():
    logging.debug("IN api_project_list_get")
    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        result = project_mgmt.get_project_list(cursor)
    response.content_type = 'application/json'
    return json.dumps(result)


########################################
# Project-Task related API calls
########################################

@route('/api/project/task/list')
def api_project_task_list_get():
    logging.debug("IN api_project_task_list_get")
    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        result = project_mgmt.get_task_list(cursor)
    response.content_type = 'application/json'
    return json.dumps(result)


########################################
# Project-Tag related API calls
########################################

@route('/api/project/tag/list')
def api_project_tag_list_get():
    logging.debug("IN api_project_tag_list_get")
    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        result = project_mgmt.get_tag_list(cursor)
    response.content_type = 'application/json'
    return json.dumps(result)


########################################
# GETs singular
########################################



########################################
# POSTs
########################################


@route('/api/project/add', method=["POST"])
def api_project_add():
    logging.debug("IN api_project_add")
    
    if request.content_type != "application/json":
        return

    json = request.json
    # Validate input data
    # Add record to database
    # import pdb
    # pdb.set_trace()

    project_name = json['project_name']
    project_category = json['project_category']
    project_status = json['project_status']
    timestamp = datetime.utcnow()

    with sqlite3.connect(project_mgmt.SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        #result = project_mgmt.get_project_list(cursor)
        project_mgmt.upsert_project(
            cursor,
            project_name,
            project_category,
            project_status,
            timestamp
        )
    response.content_type = 'application/json'
    return
    #return json.dumps(result)


########################################
# OBSOLETEs
########################################


# @route('/api/game/trading/get-info/<session_id>')
# def api_game_trading_get_info(session_id=None):
#     logging.debug("IN api_game_trading_get_info")
#     game_session = {
#         "data_type"         : "session-info",
#         "session_id"        : "yyyyMMdd",
#         "start_trade_date"  : "yyyyMMdd",
#         "user_input"        : [session_id]
#     }
#     return json.dumps(game_session)


# @route('/api/game/trading/get-price/<session_id>/<code>')
# def api_game_trading_get_price(session_id=None, code=None):
#     logging.debug("IN api_game_trading_get_price")    
#     game_session = {
#         "data_type"         : "price",
#         "session_id"        : "yyyyMMdd",
#         "start_trade_date"  : "yyyyMMdd",
#         "user_input"        : [session_id, code]
#     }
#     return json.dumps(game_session)


# @route('/api/game/trading/send-order')
# def api_game_trading_send_order(session_id=None, code=None):
#     logging.debug("IN  api_game_trading_send_order")    
#     game_session = {
#         "data_type"         : "price",
#         "session_id"        : "yyyyMMdd",
#         "start_trade_date"  : "yyyyMMdd",
#         "user_input"        : [session_id, code]
#     }
#     return json.dumps(game_session)



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