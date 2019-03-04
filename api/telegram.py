import json
import logging
import os
import pdb
import re
from helpers.app_helpers import *
from helpers.page_helpers import *
from helpers.jinja2_helpers import *
from helpers.telegram_helpers import *
#from main import *
#from flask import request

################################################################################
# Setup helper functions
################################################################################

def get_machine_status(log_string):
    rdp_re = re.compile("Machine \[(?P<box_name>.+)\] RDP session has \[(?P<box_ip>.*)\]")
    result = rdp_re.match(log_string)
    if result is None:
        return result
    box_name = result.group("box_name")
    box_ip = result.group("box_ip").split(":")[0]
    return (box_name, box_ip)

def get_box_statuses():
    cwd = os.getcwd()
    #os.path.relpath("data/box_statuses.json")
    outfile_path = os.path.join(os.getcwd(), os.path.relpath("static/data/box_statuses.json"))
    box_statuses = None
    if os.path.exists(outfile_path):
        # Read file
        with open(outfile_path, "rb") as outfile:
            json_data = outfile.read()
            box_statuses = json.loads(json_data)
    else:
        box_statuses = {}
    return box_statuses

def save_box_statuses(box_statuses):
    logging.debug("IN save_box_statuses()")
    cwd = os.getcwd()
    #os.path.relpath("data/box_statuses.json")
    outfile_path = os.path.join(os.getcwd(), os.path.relpath("static/data/box_statuses.json"))
    # Write to file
    try:
        with open(outfile_path, "w+") as outfile:
            outfile.write(json.dumps(box_statuses))
            logging.debug("Saved!")
    except Exception as ex:
        logging.error(ex)
    

def update_box_statuses(log_string):
    logging.debug("IN update_box_statuses()")
    result = get_machine_status(log_string)
    if result is not None:
        logging.debug("IN result is not None")
        # We got a machine status log entry; update json
        # Get box statues
        box_statuses = get_box_statuses()
        box_name = result[0]
        box_ip = result[1]
        logging.debug("box_name: %s, box_ip: %s" % (box_name, box_ip))
        # Update box_statuses.json
        if not box_statuses.has_key(box_name):
            box_statuses[box_name] = {}
        box_statuses[box_name]["status"] = "In use" if len(box_ip) > 0 else "Available"
        box_statuses[box_name]["comment"] = box_ip
        save_box_statuses(box_statuses)

################################################################################
# Setup routes
################################################################################

@route('/api/telegram/updates', method='POST')
def api_telegram_plato_dev_post():
    logging.debug("IN api_telegram_plato_dev_post()")
    # ZX: Support to get an Update object from the content of the response?
    # logging.info("should dump content here")
    json_data = request.json
    if json_data is None:
        return None

    try:
        logging.info(str(json_data))
        
        message_text = ""
        
        if json_data.has_key("message"):
            message_text = json_data["message"]["text"]
        
        if json_data.has_key("channel_post"):
            message_text = json_data["channel_post"]["text"]

        logging.debug("message_text is:" + message_text)
        update_box_statuses(message_text)
    except Exception as ex:
        logging.error(ex)
    #send_message(appconfig["telegram"]["token"], "53274105", "i received message")
    #return json.dumps("api_telegram_plato_dev_post")
    return str(json_data)
    #
    # cwd = os.getcwd()
    # logging.info(cwd)
    # rdp_re = re.compile("Machine \[(?P<box_name>.+)\] RDP session has \[(?P<ip>.*)\]")
    # result = rdp_re.match(str(json_data["message"]["text"]))
    # if result is None:
    #     pass
    # else:
    #     pass
    #send_message(appconfig["telegram"]["token"], "53274105", "i received message")
    #return json.dumps("api_telegram_plato_dev_post")
    # return str(json_data)


@route('/api/telegram/brahman-devops/sendMessage', method='POST')
def api_telegram_plato_dev_send_message_post():
    logging.debug("IN api_telegram_plato_dev_send_message_post()")
    
    chat_id = None
    message = None

    if 'chat_id' in request.json.keys():
        chat_id = request.json['chat_id']
    if 'message' in request.json.keys():
        message = request.json['message']
    
    if chat_id is None or message is None:
        response.set_header('Content-Type', 'application/json')
        return json.dumps("{}")

    json_response_string = send_message(appconfig["telegram"]["token"], chat_id, message)
    
    json_response_object = json.loads(json_response_string)
    response.set_header('Content-Type', 'application/json')
    return json_response_object


@route('/api/telegram/setWebhook', method='POST')
def api_telegram_set_webhook_post():
    logging.debug("IN api_telegram_set_webhook_post()")
    json_data = set_webhook(appconfig["telegram"]["token"])
    response.set_header('Content-Type', 'application/json')
    return json_data


@route('/api/telegram/getme', method='POST')
def api_telegram_getme_get():
    # 
    # {"ok": true, "result": {"username": "plato_dev_bot", "first_name": "plato-dev-bot", "is_bot": true, "id": 407476479}}
    logging.debug("IN api_telegram_getme_get()")
    json_data = get_me(appconfig["telegram"]["token"])
    response.set_header('Content-Type', 'application/json')
    return json_data

