# Bot handler for Slack bot Emmy
# 
#
################################################################################
# Imports
################################################################################

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

# N/A

################################################################################
# Setup routes
################################################################################

@route('/api/slack/emmy/updates', method='POST')
def api_slack_emmy_updates_post():
    logging.debug("IN api_slack_emmy_updates_post()")
    json_data = request.json
    logging.info(str(json_data))
    if json_data is None:
        return None
    if json_data.has_key('type'):
        # Handle url_verification event
        if json_data['type'] == "url_verification":
            return json_data['challenge']
        # Handle event_callback event
        if json_data['type'] == "event_callback":
            # if is event_callback, we should have an event
            evt = json_data['event']
    return "OK"


@route('/api/slack/emmy/say')
def api_slack_emmy_say_post():
    logging.debug("IN api_slack_emmy_say_post()")
    webhook_url = "https://hooks.slack.com/services/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"
    import requests
    r = requests.post(webhook_url, json={"text": "hello world"})
    return r.status_code
    

@route('/api/slack/emmy/test-get')
def api_slack_emmy_test_get():
    logging.debug("IN api_slack_emmy_test_post()")
    return "get-OK"

@route('/api/slack/emmy/test-post', method='POST')
def api_slack_emmy_test_post():
    logging.debug("IN api_slack_emmy_test_post()")
    return "post-OK"
