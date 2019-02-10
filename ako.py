################################################################################
# Imports
################################################################################

import json

try:
    # Python3
    from urllib.request import urlopen
except Exception:
    # Python2
    from urllib import urlopen

from datetime import datetime
from hashlib import md5
from io import StringIO
from lxml import etree

from modules import sw_news_data


################################################################################
# Common functions
################################################################################

def get_content(target_url=None):
    response_content = None
    try:
        http_response = urlopen(target_url)
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


def update_software_news(rec):
    print(rec)
    sw_news_data.update_software_news(
        rec['name'],
        rec['version'],
        rec['last_updated'],
        rec['md5_hash'],
        rec['last_checked']
    )


########################################
# Data scraping (JSON)
########################################

def scrape_nuget(): 
    target_url = 'https://dist.nuget.org/index.json'
    json_data = get_json(target_url)
    jd = json_data['artifacts'][0]['versions'][0]
    rec = mk_rec(
        'nuget', 
        jd['version'],
        jd['releasedate'],
        get_utc_date(),
        get_md5_hash(jd)
    )
    update_software_news(rec)


########################################
# Data scraping (HTML via xpath)
########################################

def scrape_nodejs():
    target_url = 'https://nodejs.org/en/'
    html_tree = get_html_tree(target_url)
    
    # nodejs has 2 versions defined on target_url: LTS and Current

    # LTS case
    target_xpath = '//*[@id="home-intro"]/div[1]/a'
    element_list = html_tree.xpath(target_xpath)
    if len(element_list) > 0:
        e = element_list[0]
        
        rec = mk_rec(
            "nodejs (lts)",
            e.get('data-version'),
            None,
            get_utc_date(),
            get_md5_hash(etree.tostring(e))
        )
        update_software_news(rec)

    # Current case
    target_xpath = '//*[@id="home-intro"]/div[2]/a'
    element_list = html_tree.xpath(target_xpath)
    if len(element_list) > 0:
        e = element_list[0]
        
        rec = mk_rec(
            "nodejs (current)",
            e.get('data-version'),
            None,
            get_utc_date(),
            get_md5_hash(etree.tostring(e))
        )
        update_software_news(rec)


if __name__ == "__main__":
    pass
    from modules import sw_news_data
    sw_news_data.init()

    scrape_nuget()
    scrape_nodejs()

    