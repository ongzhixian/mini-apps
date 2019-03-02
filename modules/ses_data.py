# Module to parse Toto data
# Data downloaded from https://en.lottolyzer.com/home/singapore/toto
################################################################################
# Import statements
################################################################################

import csv
import logging
import os
import sqlite3
from datetime import datetime
import requests
import json

################################################################################
# CONSTANT(s)
################################################################################

DATA_DIRECTORY_PATH = './data/sqlite3'
SQLITE_FILE_NAME = 'ses.sqlite3'
SQLITE_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, SQLITE_FILE_NAME)
constants = {
    DATA_DIRECTORY_PATH : './data/sqlite3',
    SQLITE_FILE_NAME : 'ses.sqlite3',
    SQLITE_FILE_PATH : os.path.join(DATA_DIRECTORY_PATH, SQLITE_FILE_NAME)
}

################################################################################
# Main function
################################################################################

########################################
# Core functions
########################################

def init():
    initialize_sqlite_db(SQLITE_FILE_PATH)

########################################
# Data download functions
########################################

REQUEST_HEADER = {
    'User-agent' : "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

def suppress_requests_warnings(active=True):
    """Suppress warning messages from requests module"""
    if active:
        # Suppress "Starting new HTTPS connection messages
        logging.getLogger("requests").setLevel(logging.WARNING)
        #Use the below if we want to suppress for urllib3 (which is used by "requests" module)
        #logging.getLogger("urllib3").setLevel(logging.WARNING)
    else:
        # Restore requests module default logging level
        logging.getLogger("requests").setLevel(logging.INFO)
        #Use the below if we want to suppress for urllib3 (which is used by "requests" module)
        #logging.getLogger("urllib3").setLevel(logging.INFO)

def get_content(target_url=None):
    """ Use requests module (http://docs.python-requests.org/en/master/user/quickstart/) to get content
        ZX: Tried using Python built-in libraries but encounter some difficulties; gave up...
    """
    response_content = None

    # suppress warnings that are displayed
    requests.packages.urllib3.disable_warnings()
    # ZX:   ideally, we only want to suppress "InsecureRequestWarning" (because we set verify=False), that is:
    #       requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    #       But that means, we need to import the "urllib3" module :-(
    #       So, let's forget about it.
    #       The reason we NEED to set verify=False is because requests will fail (no reponse) for SSL hosts not set
    #       However. if it IS set, we get a warning message like the following for every invocation:
    #           InsecureRequestWarning: Unverified HTTPS request is being made. 
    #           Adding certificate verification is strongly advised. 
    #           See: https://urllib3.readthedocs.org/en/latest/security.html

    try:
        with requests.Session() as req_session:
            http_response = req_session.get(target_url, headers=REQUEST_HEADER, verify=False)
            response_content = http_response.content
    except Exception:
        response_content = None
    return response_content


def download_file(target_url, save_file_path):
    suppress_requests_warnings()
    try:
        response_content = get_content(target_url)
        with open(save_file_path, "w+b") as outfile:
            outfile.write(response_content)
    except Exception as ex:
        print(ex)
    suppress_requests_warnings(False)


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


########################################
# Scraping functions
########################################

def get_historical_price_metadata(save=False, save_path=None):
    target_url = "https://www.sgx.com/infofeed/Apps?A=COW_Prices_Content&B=SecuritiesHistoricalPrice&C_T=20"
    pj = get_json(target_url)
    return pj
    
    # if we want to save the metadata file, we should execute something like:
    # download_file(url, 'data/ses/historical-price-metadata.json')

def get_latest_historical_price_key():
    pj = get_historical_price_metadata()
    if pj is None:
        return None
    return pj['items'][0]['key']


def download_prices(start_num=None, end_num=None, last_n_days=7, save_file_path="data/ses/prices/"):
    file_path_list = []
    if start_num is None or end_num is None:
        (start_num, end_num) = get_download_prices_start_end(last_n_days)

    if start_num is None or end_num is None:
        logging.info("start_num [{0}], end_num [{1}]; stopping download_prices".format(start_num, end_num))
        return # do nothing

    # Loop from start_num to end_num to download file by key
    curr_num = start_num
    url_template = "https://links.sgx.com/1.0.0/securities-historical/{0}/SESprice.zip"
    save_file_path_template = os.path.join(save_file_path, "SESprice-{0}.zip")
    while curr_num <= end_num:
        try:
            curr_url = url_template.format(curr_num)
            curr_save_file_path = save_file_path_template.format(curr_num)
            download_file(curr_url, curr_save_file_path)
            file_path_list.append(curr_save_file_path)
            logging.info("Downloaded price for key[{0}] to [{1}]".format(curr_num, curr_save_file_path))
            curr_num = curr_num + 1
        except Exception as ex:
            logging.error(ex)
    return (start_num, end_num, file_path_list)

def get_download_prices_start_end(last_n_days=7):
    end_num = int(get_latest_historical_price_key())
    start_num = end_num - last_n_days
    return (start_num, end_num)

def download_isin():
    url = "https://links.sgx.com/1.0.0/isin/1/"
    # The above url will resolve to an url like the below:
    # https://links.sgx.com/FileOpen/22%20Feb%202019.ashx?App=ISINCode&FileID=1
    output_file_path = "data/ses/isin-{0}.dat".format(datetime.now().strftime("%Y%m%d"))
    download_file(url, output_file_path)
    logging.info("Download ISIN to {0}".format(output_file_path))
    return output_file_path

def process_isin_file(input_file_path):
    current_timestamp = datetime.now().strftime("%Y-%m-%d")
    with open(input_file_path, "r") as f:
        f.readline()
        lines = f.readlines()
    # Layout of ISIN file.
    # Field   Width
    # Name        50
    # Status      10
    # ISIN Code   20
    # Code        10
    # Name        50
    # for line_data in lines:
    #     name = line_data[:50].strip()
    #     status = line_data[50:60].strip()
    #     isin_code = line_data[60:80].strip()
    #     code = line_data[80:90].strip()
    #     counter_name = line_data[90:].strip()
    #     logging.debug("Updating ISIN for [{0}]".format(code))
    # ZX: Connecting on every upsert is too slow! Especially on Windows/Python3.7
    #     upsert_isin(SQLITE_FILE_PATH, code, name, status, isin_code, counter_name, current_timestamp)
    with sqlite3.connect(SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        for line_data in lines:
            name = line_data[:50].strip()
            status = line_data[50:60].strip()
            isin_code = line_data[60:80].strip()
            code = line_data[80:90].strip()
            counter_name = line_data[90:].strip()
            cursor.execute(
                "INSERT OR REPLACE INTO isin (code, name, status, isin_code, counter_name, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (code, name, status, isin_code, counter_name, current_timestamp)
                )
            logging.debug("Updating ISIN for [{0}]".format(code))
    logging.info("Number of lines processed: [{0}]".format(len(lines)))

def process_price_file(input_file_path):
    current_timestamp = datetime.now().strftime("%Y-%m-%d")

    with open (input_file_path, 'r') as f:
        # csv   - comma separated values
        # ssv  - semi-colon separated values
        #line = f.readline() # skip header (if any)
        row_num = 0
        price_reader = csv.reader(f, delimiter=';')
        with sqlite3.connect(SQLITE_FILE_PATH) as conn:
            cursor = conn.cursor()
            for row in price_reader:
                if len(row) < 16:
                    logging.warning("Skipping line; row has lesser than 16 fields: [%s]" %  row)
                    break
                upsert_price(cursor, row)
                row_num = row_num + 1

        # If no rows are processed, probably because format is old format (comma-separated instead of semi-colon)    
    if row_num == 0:
        with open (input_file_path, 'r') as f:  
            price_reader = csv.reader(f, delimiter=',')
            with sqlite3.connect(SQLITE_FILE_PATH) as conn:
                cursor = conn.cursor()
                for row in price_reader:
                    if len(row) >= 15:
                        upsert_price_old(cursor, row)
                        row_num = row_num + 1
                    elif len(row) == 13:
                        upsert_price_old12(cursor, row)
                        row_num = row_num + 1
                    elif len(row) > 0 and row[0] == '\x1a':
                        continue
                    else:
                        logging.warning("Skipping line; row has lesser than 13 fields: [%s]" %  row)
                        import pdb
                        pdb.set_trace()
                        break
                    # upsert_price_old(cursor, row)
                    # row_num = row_num + 1

        if row_num == 0:
            logging.warning("FILE NOT PROCESSED: [{0}]".format(input_file_path))
        logging.info("[{0}] has [{1}] rows processed.".format(input_file_path, row_num))
        input_file_name = os.path.basename(input_file_path)
        upsert_processed_file(cursor, input_file_name, input_file_path, "PRICE", row[0], current_timestamp, None)


# def download_prices():
#     end_num = 5385
#     start_num = 4779
#     curr_num = start_num
#     #url = "https://links.sgx.com/1.0.0/securities-historical/5385/SESprice.dat"
#     url_template = "https://links.sgx.com/1.0.0/securities-historical/{0}/SESprice.dat"
#     save_file_path_template = "data/ses/SESprice-{0}.dat"

#     while curr_num < end_num:
#         curr_url = url_template.format(curr_num)
#         curr_save_file_path = save_file_path_template.format(curr_num)
#         download_file(curr_url, curr_save_file_path)
#         print(curr_url)
#         print(curr_save_file_path)
#         curr_num = curr_num + 1
        




def load_csv(csv_path):
    results = []
    with open(csv_path, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        csv_reader.next() # Use next() to rows such as headers
        for row in csv_reader:
            results.append(row)
    return results

def csv_to_db(csv_path):

    with open(csv_path, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        csv_reader.next() # Use next() to rows such as headers
        with sqlite3.connect(SQLITE_FILE_PATH) as conn:
            cursor = conn.cursor()
            for row in csv_reader:
                #results.append(row)
                exec_cursor = add_raw(
                    cursor, 
                    row[0], # draw_number
                    row[1], # draw_date
                    row[2], # num1
                    row[3], # num2
                    row[4], # num3
                    row[5], # num4
                    row[6], # num5
                    row[7], # num6
                    row[8], # num7
                    ''      # remarks
                    )

                # The CSV data file we have only have prize winner information after
                if len(row) > 18:
                    add_winner(cursor, row[0], row[1], '1', row[18], row[19], '')
                    add_winner(cursor, row[0], row[1], '2', row[20], row[21], '')
                    add_winner(cursor, row[0], row[1], '3', row[22], row[23], '')
                    add_winner(cursor, row[0], row[1], '4', row[24], row[25], '')
                    add_winner(cursor, row[0], row[1], '5', row[26], row[17], '')
                    add_winner(cursor, row[0], row[1], '6', row[28], row[29], '')

                if len(row) > 30:
                    # Division 7 was only introduced on 2014-10-06
                    # Prior to that, there were only 6 prize divisions
                    add_winner(cursor, row[0], row[1], '7', row[30], row[31], '')
                
                logging.debug("Add draw number {0}, {1}".format(row[0], exec_cursor.rowcount))

        # end with sqlite3.connect(SQLITE_FILE_PATH) as conn:
    # end with open(csv_path, 'rb') as csvfile:


############################################################
# Sqlite3 related functions
############################################################

########################################
# isin table functions
########################################

def create_isin_table(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    """
    CODE
    NAME
    STATUS
    ISIN CODE
    TRADING COUNTER NAME
    """
    return sqlite3_cursor.execute('''CREATE TABLE IF NOT EXISTS isin (
        code                text,
        name                text,
        status              text,
        isin_code           text,
        counter_name        text,
        timestamp           text,
        PRIMARY KEY (code)
        )''')

def upsert_isin(sqlite_filename, code, name, status, isin_code, counter_name, timestamp):
    with sqlite3.connect(sqlite_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO isin (code, name, status, isin_code, counter_name, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (code, name, status, isin_code, counter_name, timestamp)
            )

########################################
# price table functions
########################################

def create_price_table(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    """
    TRADE DATE  (YYYY-MM-DD)
    STOCK NAME  (30 chars)
    REMARKS     (8 chars) SUSP - Suspended   
    CURRENCY    (4 chars)
    HIGH        (7 chars, including decimal point)
    LOW         (7 chars, including decimal point)
    LAST        (7 chars, including decimal point)
    CHANGE      (7 chars, including sign & decimal point)
    VOLUME      (10 chars)
    BID         (9 chars, including sign & decimal point)
    OFFER       (9 chars, including sign & decimal point)
    MARKET      (13 chars)
    OPEN        (7 chars, including decimal point)
    VALUE       (11 chars)
    STOCK CODE  (4 chars)
    DClose      (7 chars, including decimal point)   
    """
    return sqlite3_cursor.execute('''CREATE TABLE IF NOT EXISTS price (
        trade_date  text,
        stock_name  text,
        remarks     text,
        currency    text,
        high        numeric,
        low         numeric,
        last        numeric,
        change      numeric,
        volume      text,
        bid         numeric,
        offer       numeric,
        market      text,
        open        numeric,
        value       text,
        stock_code  text,
        dclose      numeric,
        PRIMARY KEY (trade_date, stock_code)
        )''')

def upsert_price(cursor, sv_row):
    # #update_company_table(appconfig["sqlite"]["sgx_db"], row)
    # update_price_table(appconfig["sqlite"]["sgx_db"], row)
    # logging.debug("DO row")
    # row_num = row_num + 1
    # timestamp   = row[0].strip()
    # code        = row[14].strip()
    # mkt_open    = row[12].strip()
    # mkt_high    = row[4].strip()
    # mkt_low     = row[5].strip()
    # mkt_close   = row[6].strip()
    # bid         = row[9].strip()
    # ask         = row[10].strip()
    # volume      = row[8].strip()
    # value       = row[13].strip()
    f_trade_date  = sv_row[0].strip()
    f_stock_name  = sv_row[1].strip()
    f_remarks     = sv_row[2].strip()
    f_currency    = sv_row[3].strip()
    f_high        = sv_row[4].strip()
    f_low         = sv_row[5].strip()
    f_last        = sv_row[6].strip()
    f_change      = sv_row[7].strip()
    f_volume      = sv_row[8].strip()
    f_bid         = sv_row[9].strip()
    f_offer       = sv_row[10].strip()
    f_market      = sv_row[11].strip()
    f_open        = sv_row[12].strip()
    f_value       = sv_row[13].strip()
    f_stock_code  = sv_row[14].strip()
    f_dclose      = sv_row[15].strip()
    #logging.debug(f_trade_date, f_stock_name, f_remarks, f_currency, f_high, f_low, f_last, f_change, f_volume, f_bid, f_offer, f_market, f_open, f_value, f_stock_code, f_dclose)
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO price (trade_date, stock_name, remarks, currency, high, low, last, change, volume, bid, offer, market, open, value, stock_code, dclose) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (f_trade_date, f_stock_name, f_remarks, f_currency, f_high, f_low, f_last, f_change, f_volume, f_bid, f_offer, f_market, f_open, f_value, f_stock_code, f_dclose)
            )
    except Exception as ex:
        logging.error(ex)

def upsert_price_old(cursor, sv_row):
    f_trade_date  = sv_row[0].strip()
    f_stock_name  = sv_row[1].strip()
    f_remarks     = sv_row[2].strip()
    f_currency    = sv_row[3].strip()
    f_high        = sv_row[4].strip()
    f_low         = sv_row[5].strip()
    f_last        = sv_row[6].strip()
    f_change      = sv_row[7].strip()
    f_volume      = sv_row[8].strip()
    f_bid         = sv_row[9].strip()
    f_offer       = sv_row[10].strip()
    f_market      = sv_row[11].strip()
    f_open        = sv_row[12].strip()
    f_value       = sv_row[13].strip()
    f_stock_code  = sv_row[14].strip()
    #f_dclose      = sv_row[15].strip()
    #logging.debug(f_trade_date, f_stock_name, f_remarks, f_currency, f_high, f_low, f_last, f_change, f_volume, f_bid, f_offer, f_market, f_open, f_value, f_stock_code, f_dclose)
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO price (trade_date, stock_name, remarks, currency, high, low, last, change, volume, bid, offer, market, open, value, stock_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (f_trade_date, f_stock_name, f_remarks, f_currency, f_high, f_low, f_last, f_change, f_volume, f_bid, f_offer, f_market, f_open, f_value, f_stock_code)
            )
    except Exception as ex:
        logging.error(ex)


def upsert_price_old12(cursor, sv_row):
    f_trade_date  = sv_row[0].strip()
    f_stock_name  = sv_row[1].strip()
    f_remarks     = sv_row[2].strip()
    f_currency    = sv_row[3].strip()
    f_high        = sv_row[4].strip()
    f_low         = sv_row[5].strip()
    f_last        = sv_row[6].strip()
    f_change      = sv_row[7].strip()
    f_volume      = sv_row[8].strip()
    f_bid         = sv_row[9].strip()
    f_offer       = sv_row[10].strip()
    f_market      = sv_row[11].strip()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO price (trade_date, stock_name, remarks, currency, high, low, last, change, volume, bid, offer, market) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (f_trade_date, f_stock_name, f_remarks, f_currency, f_high, f_low, f_last, f_change, f_volume, f_bid, f_offer, f_market)
            )
    except Exception as ex:
        logging.error(ex)


########################################
# price table functions
########################################

def create_processed_file_table(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    """
    """
    return sqlite3_cursor.execute('''CREATE TABLE IF NOT EXISTS processed_file (
        file_name   text,
        file_path   text,
        file_type   text,
        trade_date  text,
        timestamp   text,
        remarks     text,
        PRIMARY KEY (file_path)
        )''')

def upsert_processed_file(cursor, file_name, file_path, file_type, trade_date, timestamp, remarks):
    cursor.execute(
        "INSERT OR REPLACE INTO processed_file (file_name, file_path, file_type, trade_date, timestamp, remarks) VALUES (?, ?, ?, ?, ?, ?)",
        (file_name, file_path, file_type, trade_date, timestamp, remarks)
        )



########################################
# raw table functions
########################################

def create_raw_table(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    return sqlite3_cursor.execute('''CREATE TABLE IF NOT EXISTS raw (
        draw_number         numeric ,
        draw_date           text,
        num1                numeric,
        num2                numeric,
        num3                numeric,
        num4                numeric,
        num5                numeric,
        num6                numeric,
        num7                numeric,
        remarks             text,
        PRIMARY KEY (draw_number)
        )''')

def add_raw(sqlite3_cursor, draw_number, draw_date, num1, num2, num3, num4, num5, num6, num7, remarks):
    return sqlite3_cursor.execute(
        "INSERT OR REPLACE INTO raw (draw_number, draw_date, num1, num2, num3, num4, num5, num6, num7, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (draw_number, draw_date, num1, num2, num3, num4, num5, num6, num7, remarks)
    )


########################################
# winner table functions
########################################

def create_winner_table(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    return sqlite3_cursor.execute('''CREATE TABLE IF NOT EXISTS winner (
        draw_number         numeric ,
        draw_date           text,
        division            text,
        winner_count        numeric,
        prize               numeric,
        remarks             text,
        PRIMARY KEY (draw_number, division)
        )''')
    
def add_winner(sqlite3_cursor, draw_number, draw_date, division, winner_count, prize, remarks):
    return sqlite3_cursor.execute(
        "INSERT OR REPLACE INTO winner (draw_number, draw_date, division, winner_count, prize, remarks) VALUES (?, ?, ?, ?, ?, ?)",
        (draw_number, draw_date, division, winner_count, prize, remarks)
    )


########################################
# create views
########################################

def create_winner_summary_view(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS winner_summary AS
SELECT 	draw_number, draw_date,
		SUM(case when w.division = '1' then winner_count end) AS 'd1_cnt',
		SUM(case when w.division = '1' then prize end) AS 'd1_amt',
		SUM(case when w.division = '2' then winner_count end) AS 'd2_cnt',
		SUM(case when w.division = '2' then prize end) AS 'd2_amt',
		SUM(case when w.division = '3' then winner_count end) AS 'd3_cnt',
		SUM(case when w.division = '3' then prize end) AS 'd3_amt',
		SUM(case when w.division = '4' then winner_count end) AS 'd4_cnt',
		SUM(case when w.division = '4' then prize end) AS 'd4_amt',
		SUM(case when w.division = '5' then winner_count end) AS 'd5_cnt',
		SUM(case when w.division = '5' then prize end) AS 'd5_amt',
		SUM(case when w.division = '6' then winner_count end) AS 'd6_cnt',
		SUM(case when w.division = '6' then prize end) AS 'd6_amt',
		SUM(case when w.division = '7' then winner_count end) AS 'd7_cnt',
		SUM(case when w.division = '7' then prize end) AS 'd7_amt'
FROM 	winner w
GROUP BY 
		w.draw_number
ORDER BY 
		w.draw_number DESC;
        ''')

def create_raw49_view(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS raw49 AS
SELECT 	* 
FROM 	raw 
WHERE 	draw_date >= '2014-10-17' 
ORDER BY 
		draw_number DESC;
        ''')

def create_raw49_period_view(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS raw49_period AS
SELECT 	MIN(draw_date)	    AS 'min_draw_date', 
		MIN(draw_number)    AS 'min_draw_number', 
		MAX(draw_date)      AS 'max_draw_date', 
		MAX(draw_number)    AS 'max_draw_number'
FROM 	raw49;
        ''')

def create_toto49_view(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS toto49 AS
SELECT 	r.draw_number
		, r.draw_date
		, r.num1
		, r.num2
		, r.num3
		, r.num4
		, r.num5
		, r.num6
		, r.num7
		, ws.d1_cnt
		, ws.d1_amt
		, ws.d2_cnt
		, ws.d2_amt
		, ws.d3_cnt
		, ws.d3_amt
		, ws.d4_cnt
		, ws.d4_amt
		, ws.d5_cnt
		, ws.d5_amt
		, ws.d6_cnt
		, ws.d6_amt
		, ws.d7_cnt
		, ws.d7_amt
FROM 	raw r 
INNER JOIN 
		winner_summary ws
		ON r.draw_number = ws.draw_number
WHERE	r.draw_number >= 2998 
ORDER BY 
		r.draw_number;
        ''')


def create_last_draw_view(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS last_draw AS
SELECT 	* 
FROM 	toto49 
WHERE 	draw_number = (SELECT MAX(draw_number) FROM toto49);
        ''')



########################################
# Query function(s)
########################################

def get_last_draw():
    SQL_QUERY = """
    SELECT * FROM last_draw;
    """
    print(SQLITE_FILE_PATH)
    with sqlite3.connect(SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        result = cursor.fetchall()
    return result


# Placeholder sample for querying with parameter
# def get_instruments(sqlite_filename, sector_name):
#     SQL_QUERY = """
#     SELECT * FROM mainboard_instrument WHERE sector = ? ORDER BY volume DESC, last DESC LIMIT 15;
#     """
#     with sqlite3.connect(sqlite_filename) as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             SQL_QUERY,
#             (sector_name,)
#         )
#         result = cursor.fetchall()
#     return result



########################################
# core function(s)
########################################

def initialize_sqlite_db(sqlitedb_path):
    """Initialize a sqlite3 database for tracking ASX sector indices.

    Table(s) created:

    1.  raw
    1.  winner

    Args:
        N/A

    Returns:
        N/A
    """
    logging.info("Ensuring existence of sqlite3 database [{0}]".format(sqlitedb_path))
    with sqlite3.connect(sqlitedb_path) as conn:
        cursor = conn.cursor()
        create_isin_table(cursor)
        create_price_table(cursor)
        create_processed_file_table(cursor)
        # create_raw_table(cursor)
        # create_winner_table(cursor)
        # create_winner_summary_view(cursor)
        # create_raw49_view(cursor)
        # create_raw49_period_view(cursor)
        # create_toto49_view(cursor)
        # create_last_draw_view(cursor)
        

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    initialize_sqlite_db(SQLITE_FILE_PATH)
