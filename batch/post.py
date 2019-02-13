import sys

if sys.version_info[0] < 3:
    # Python2
    from urllib import urlencode
    from urllib2 import urlopen, Request
    # from urllib2 import Request
else:
    # Python3
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
    # from urllib.request import Request

import json

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
    res = http_post(target_url)
    print(res)
