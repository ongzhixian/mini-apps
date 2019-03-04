################################################################################
# Modules and functions import statements
################################################################################

import logging
import json
import sys

################################################################################
# Function decorators
################################################################################

################################################################################
# Basic functions
################################################################################

########################################
# Define core functions
########################################

def get_me(token):
    urlString = "https://api.telegram.org/bot%s/getme" % token
    if sys.version_info.major < 3:
        import urllib2
        req = urllib2.Request(urlString)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        result = response.read()
        response.close()
        return json.loads(result)
    else:
        import urllib.request
        req = urllib.request.Request(urlString)
        with urllib.request.urlopen(req) as response:
            json_data = response.read()
            return json_data


def send_message(token, chat_id, text):
    urlString = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (token, chat_id, urlEncodedText)
    if sys.version_info.major < 3:
        import urllib2
        req = urllib2.Request(urlString)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        result = response.read()
        response.close()
        return json.loads(result)
    else:
        import urllib.request
        urlEncodedText = urllib.request.quote(text)
        req = urllib.request.Request(urlString)
        with urllib.request.urlopen(req) as response:
            json_data = response.read()
            return json_data


        
def set_webhook(token):
    if sys.version_info.major < 3:
        pass
    else:
        import urllib.request
        urlString = "https://api.telegram.org/bot%s/setWebhook" % token
        req = urllib.request.Request(urlString)
        with urllib.request.urlopen(req) as response:
            json_data = response.read()
            return json_data

################################################################################
# Variables dependent on Application basic functions
################################################################################

# openOpc = OpenOPC.client()
# opc_clients = opc_clients(openOpc)

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    pass