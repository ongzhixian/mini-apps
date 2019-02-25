################################################################################
# Imports
################################################################################

import os
import sys
import json

import requests
from datetime import datetime, date, timedelta

from hashlib import md5
from io import StringIO
from lxml import etree

import logging
from zipfile import ZipFile

from modules import sw_news_data

################################################################################
# Setup logging configuration
################################################################################

# Setup format of logging message
logging_format = '%(asctime)-15s %(levelname)-8s %(message)s'
#logging_format = '%(asctime)-15s %(levelname)-8s %(module)-16s %(funcName)-24s %(message)s'

# Do console logging only
#logging.basicConfig(level=logging.INFO, format=logging_format) # Console logging only

# Comment out the above block and uncomment the below block if we want console AND file logging
logging.basicConfig(filename='ses-prices-scrape.log', level=logging.DEBUG, format=logging_format) # Log to file
console_logger = logging.StreamHandler() # Log to console as well
console_logger.setFormatter(logging.Formatter(logging_format))
logging.getLogger().addHandler(console_logger)

################################################################################
# Common functions
################################################################################

REQUEST_HEADER = {
    'User-agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

def download_file(target_url, save_file_path):
    with requests.Session() as req_session:
        response = req_session.get(target_url, headers=REQUEST_HEADER, verify=False)
    with open(save_file_path, "w+b") as outfile:
        outfile.write(response.content)

def get_content(target_url=None):
    
    response_content = None

    try:
        requests.packages.urllib3.disable_warnings()
        with requests.Session() as req_session:
            http_response = req_session.get(target_url, headers=REQUEST_HEADER, verify=False)
            response_content = http_response.content
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


if __name__ == "__main__":
    pass
    from modules import ses_data
    ses_data.init()

    logging.info("[PROGRAM START]")

    # ISIN is not updated that regularly; we only want to run this occasionally
    # Since we do not have the definition of "occasionally", skipped for now
    logging.info("[ISIN] - Skipping loading and processing of ISIN")
    # filepath = ses_data.download_isin()
    # ses_data.process_isin_file(filepath)

    logging.info("[PRICE]")
    # tp = ses_data.download_prices(save_file_path="C:/src/downloads/ses") # tp - tuple; tp = (start_num, end_num, file_path_list)
    # file_path_list = tp[2]
    # if file_path_list is not None and len(file_path_list) > 0:
    #     for file_path in file_path_list:
    #         ses_data.process_price_file(file_path)

    # Test
    # file1 = file_path_list[0]
    # bn = os.path.basename(file1)
    #ses_data.process_price_file(file1)

    # Process zipped archived files (old)
    #raw_prices_dir = "data/ses/raw-prices"
    raw_prices_dir = "C:/src/downloads/ses"
    # SESprice-5388.zip
    start_num = 5388
    curr_num = start_num 
    while curr_num > 0:
        curr_zipped_file_name = "SESprice-{0}.zip".format(curr_num)
        zipped_price_file_path = os.path.join(raw_prices_dir, curr_zipped_file_name)
        logging.info("Processing [{0}]".format(zipped_price_file_path))
        try:
            # create directory for zipfile content extraction
            output_dir_name = "SESprice-{0}".format(curr_num)
            extract_dirpath = 'C:/src/temp/ses/{0}'.format(output_dir_name)
            if not os.path.exists(extract_dirpath):
                os.makedirs(extract_dirpath)
            # unzip file
            with ZipFile(zipped_price_file_path, 'r') as myzip:
                myzip.extractall(extract_dirpath)
            # process the SESPRICE.DAT in each directory
            # TODO:
            curr_num = curr_num - 1
        except Exception as ex:
            logging.error(ex)
        # try:
        #     ses_data.process_price_file(price_file_path)
        # except Exception as ex:
        #     logging.exception("Fail to process file: [{0}]".format(price_file_path))


    # Process archived files (old)
    # raw_prices_dir = "data/ses/raw-prices"
    # file_list = os.listdir(raw_prices_dir)

    # for file_name in file_list:
    #     price_file_path = os.path.join(raw_prices_dir, file_name)
    #     logging.info("Processing [{0}]".format(price_file_path))
    #     try:
    #         ses_data.process_price_file(price_file_path)
    #     except Exception as ex:
    #         logging.exception("Fail to process file: [{0}]".format(price_file_path))

    #print(file_list[0])


    logging.info("[PROGRAM END]")


    # # https://api2.sgx.com/content-api?queryId=9756cc24703868bca7da492a8e1aebd1268eaf70:alerts&variables={"lang":"EN"}
    # # "https://www.sgx.com/infofeed/Apps?A=COW_Prices_Content&&B=SecuritiesHistoricalPrice&F=5370&G=SESprice.dat"
    # # https://www.sgx.com/infofeed/Apps?A=COW_Prices_Content&B=SecuritiesHistoricalPrice&F=5370&G=SESprice.dat&H=2019-01-28
    # "https://links.sgx.com/1.0.0/securities-historical/5385/SESprice.dat"
    # "http://links.sgx.com/1.0.0/securities-historical/5385/SESprice.dat"
    # #download_json(url, "data/ses/list.json")

    # Demo code to get JSON from url
    # url = "https://www.sgx.com/infofeed/Apps?A=COW_Prices_Content&B=SecuritiesHistoricalPrice&C_T=20"
    # js = get_json(url)
    # key = js['items'][0]['key']
    # print(key)
    
    # Demo code to download JSON from url to specified path
    # ses_data.download_file(url, 'data/ses/historical-price-metadata.json')

    # lk = ses_data.get_latest_historical_price_key()
    # print(lk)


    #ses_data.download_prices()

    

    # (?<name>.{50})(?<status>.{10})(?<isin>.{20})(?<code>.{10})(?<counter_name>.+)


    # response_content = get_content(url)
    # print(response_content)
    # with requests.Session() as req_session:
    #     requests.packages.urllib3.disable_warnings()
    #     response = req_session.get(url, headers=REQUEST_HEADER, verify=False)
    #     print(response)
        #print(response.content)


    
    #open('google.ico', 'wb').write(r.content)


    
    # 
    # end_num = 5385
    # start_num = 4779
    # curr_num = start_num
    # #url = "https://links.sgx.com/1.0.0/securities-historical/5385/SESprice.dat"
    # url_template = "https://links.sgx.com/1.0.0/securities-historical/{0}/SESprice.dat"
    # save_file_path_template = "data/ses/SESprice-{0}.dat"

    # while curr_num < end_num:
    #     curr_url = url_template.format(curr_num)
    #     curr_save_file_path = save_file_path_template.format(curr_num)
    #     download_file(curr_url, curr_save_file_path)
    #     print(curr_url)
    #     print(curr_save_file_path)
    #     curr_num = curr_num + 1
        

