
# Packages used
# pip install beautifulsoup4
# pip install lxml
# pip install feedparser
# [OPTIONAL] pip install html5lib


# import urllib2

# target_url = 'https://www.nuget.org/downloads'

# import requests
# from bs4 import BeautifulSoup

# #r = requests.get('https://api.github.com', auth=('user', 'pass'))
# r = requests.get(target_url)

# soup = BeautifulSoup(r.content)

# #print r.status_code
# #print r.headers['content-type']


# from lxml import etree

# target_xpath = '//*[@id="stage-dynamic"]/div[2]/div[1]/div/ul/li[1]/a/span[1]'

# htmlparser = etree.HTMLParser()
# #from StringIO import StringIO
# from io import StringIO
# tree = etree.parse(StringIO(r.text), htmlparser)
# tree.xpath(target_xpath)

import json
import urllib.request

from datetime import datetime
from hashlib import md5
from io import StringIO
from lxml import etree

################################################################################
# Common functions
################################################################################

def get_content(target_url=None):
    response_content = None
    try:
        http_response = urllib.request.urlopen(target_url)
        response_content = http_response.read()
    except Exception:
        response_content = None
    
    return response_content

def get_json(target_url=None):
    json_data = None
    
    try:
        response_content = get_content(target_url)
        if response_content is None:
            return json_data

        json_data = json.loads(response_content)
    except Exception:
        json_data = None
    
    return json_data

def get_html_tree(target_url=None):
    html_tree = None
    
    try:
        response_content = get_content(target_url)
        if response_content is None:
            return html_tree

        html_parser = etree.HTMLParser()
        html_tree = etree.parse(StringIO(response_content.decode('utf-8')), html_parser)
        
    except Exception:
        html_tree = None
    
    return html_tree



################################################################################
# Data scraping (JSON)
################################################################################

def get_md5_hash(strVal):
    return md5(str(strVal).encode('utf-8')).hexdigest()

def get_utc_date():
    return datetime.utcnow().strftime("%Y-%m-%d")


def mk_rec(name, version, last_updated, last_checked, md5_hash):
    return {
        'name': name,
        'version': version,
        'last_updated': last_updated,
        'last_checked': last_checked,
        'md5_hash': md5_hash
    }


def scrape_nuget():
    target_url = 'https://dist.nuget.org/index.json'
    json_data = get_json(target_url)
    jd = json_data['artifacts'][0]['versions'][0]
    rec = mk_rec(
        'nuget.exe', 
        jd['version'],
        jd['releasedate'],
        get_utc_date(),
        get_md5_hash(jd)
        )
    print(rec)
    return rec


if __name__ == "__main__":
    pass
    #scrape_nuget()

    # target_url = 'https://nodejs.org/en/'
    # t = get_content(target_url)
    # htmlparser = etree.HTMLParser()
    # tree = etree.parse(StringIO(t.decode('utf-8')), htmlparser)

    # # LTS
    # target_xpath = '//*[@id="home-intro"]/div[1]/a'
    # # Current
    # elementList = tree.xpath(target_xpath)

    # scrape nodejs
    target_url = 'https://nodejs.org/en/'
    html_tree = get_html_tree(target_url)

    # nodejs has LTS and Current

    # LTS case
    target_xpath = '//*[@id="home-intro"]/div[1]/a'
    element_list = html_tree.xpath(target_xpath)
    if len(element_list) > 0:
        e = element_list[0]
        
        lts_rec = mk_rec(
            "nodejs (lts)",
            e.get('data-version'),
            None,
            get_utc_date(),
            get_md5_hash(etree.tostring(e))
        )
        print(lts_rec)

    # Current case
    target_xpath = '//*[@id="home-intro"]/div[2]/a'
    element_list = html_tree.xpath(target_xpath)
    if len(element_list) > 0:
        e = element_list[0]
        
        current_rec = mk_rec(
            "nodejs (current)",
            e.get('data-version'),
            None,
            get_utc_date(),
            get_md5_hash(etree.tostring(e))
        )
        print(current_rec)


    #print(t)
