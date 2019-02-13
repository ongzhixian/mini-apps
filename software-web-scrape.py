################################################################################
# Imports
################################################################################

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


def http_post(url, data_dict):
    request_headers = {"Content-Type": "application/json"}
    request = Request(url, data=json.dumps(data_dict).encode('utf-8'), headers=request_headers)
    response = urlopen(request)
    return response.read()


def update_software_news(rec):
    print(rec)
    #target_url = "http://localhost:50001/api/software/news"
    target_url = "http://mini-apps.plato.emptool.com/api/software/news"
    http_post(target_url, rec)
    # sw_news_data.update_software_news(
    #     rec['name'],
    #     rec['version'],
    #     rec['last_updated'],
    #     rec['md5_hash'],
    #     rec['last_checked']
    # )


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


def scrape_dotnet():
    target_url = 'https://dotnet.microsoft.com/download?initial-os=windows'
    html_tree = get_html_tree(target_url)

    # target_url has define the following software version defined:
    # .NET Framework
    # .NET CORE SDK
    # .NET CORE Runtime

    target_xpath = '/html/body/div[4]/div[3]/div[1]/div[2]/h2'
    element_list = html_tree.xpath(target_xpath)
    if len(element_list) > 0:
        e = element_list[0]
        #print(e.text)
        rec = mk_rec(
            ".NET Framework",
            e.text.replace('.NET Framework','').strip(),
            None,
            get_utc_date(),
            get_md5_hash(etree.tostring(e))
        )
        update_software_news(rec)
    
    target_xpath = '/html/body/div[4]/div[3]/div[2]/table[1]/thead/tr/th[2]/text()[2]'
    element_list = html_tree.xpath(target_xpath)
    if len(element_list) > 0:
        e = element_list[0]
        #print(e.strip())
        rec = mk_rec(
            ".NET CORE SDK",
            e.strip(),
            None,
            get_utc_date(),
            get_md5_hash(e.strip())
        )
        update_software_news(rec)

    target_xpath = '/html/body/div[4]/div[3]/div[2]/table[1]/thead/tr/th[3]/text()[2]'
    element_list = html_tree.xpath(target_xpath)
    if len(element_list) > 0:
        e = element_list[0]
        #print(e.strip())
        rec = mk_rec(
            ".NET CORE Runtime",
            e.strip(),
            None,
            get_utc_date(),
            get_md5_hash(e.strip())
        )
        update_software_news(rec)


if __name__ == "__main__":
    pass
    from modules import sw_news_data
    sw_news_data.init()

    scrape_nuget()
    scrape_nodejs()
    scrape_dotnet()
