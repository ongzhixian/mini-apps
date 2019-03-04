import sys
import requests
import json
import urllib

def http_post(url):

    request_headers = {"Content-Type": "application/json"}
    request_data = {
        'name': 'Michael Foord',
        'location': 'Northampton',
        'language': 'Python' 
    }

    req = Request(url, data=json.dumps(request_data).encode('utf-8'), headers=request_headers)
    response = urlopen(req)
    return response.read()

if __name__ == "__main__":
    target_url = "http://localhost:50001/api/software/news"
    dst_chat_id="-1001114131130"
    token="416208415:AAEfO6AoW5yXqLZzQHZabuV1ZFFYnLo0g8E"
    #token = "bot407476479:AAEUMPVyYt6Mfg_a5EEz3VBY55TsJ-bV9iI"
    
    message = "tset msg from py"
    #"https://api.telegram.org/bot$token/sendMessage?chat_id=$dst_chat_id&text=$escapedMessageText"
    qs_params = { 
        'chat_id' : dst_chat_id,
        'text' : message
    }
    #https://api.telegram.org/bot407476479:AAEUMPVyYt6Mfg_a5EEz3VBY55TsJ-bV9iI/sendMessage?chat_id=-1001130893162&text=hello world

    if sys.version_info[0] < 3:
        # Python2
        qs = urllib.urlencode(qs_params)
    else:
        # Python3
        qs = urllib.parse.urlencode(qs_params)
        
    url = "https://api.telegram.org/bot{0}/sendMessage?{1}".format(token, qs)
    print(url)
    r = requests.get(url)
    r.status_code
    print(r)