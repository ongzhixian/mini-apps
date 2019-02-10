from urllib import urlencode
import urllib2
import json

def http_post(url):
    #post = urlencode(data)
    
    request_headers = {"Content-Type": "application/json"}
    request_data = {
        'name': 'Michael Foord',
        'location': 'Northampton',
        'language': 'Python' 
    }
    

    req = urllib2.Request(url, data=json.dumps(request_data), headers=request_headers)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == "__main__":
    target_url = "http://localhost:50001/api/software/news"
    http_post(target_url)
