# Mine content from url_kb.sqlite3
################################################################################
# Import statements
################################################################################

import hashlib
import json
import logging
import pdb
import os
import sqlite3

# import random
# import threading
# import time
import uuid

from urlparse import urlparse

from datetime import datetime
#from helpers.app_helpers import *
#from helpers.app_helpers import *

################################################################################
# Setup logging configuration
################################################################################

logging_format = '%(asctime)-15s %(levelname)-8s %(message)s'
#logging_format = '%(asctime)-15s %(levelname)-8s %(module)-16s %(funcName)-24s %(message)s'
logging.basicConfig(filename='url-kb-mine.log', level=logging.DEBUG, format=logging_format) # Log to file
console_logger = logging.StreamHandler() # Log to console as well
console_logger.setFormatter(logging.Formatter(logging_format))
logging.getLogger().addHandler(console_logger)

########################################
# Define agnostic functions
########################################

def get_appconfig(repo_root_path):
    app_config_filename = 'app_config.json'
    app_config_filepath = os.path.join(repo_root_path, app_config_filename)
    logging.debug("Opening file {0}".format(app_config_filename))
    appconfig_file = open( app_config_filepath )
    logging.debug("Loading file {0}".format(app_config_filename))
    appconfig = json.load( appconfig_file )
    logging.debug("app_config loaded")
    return appconfig

################################################################################
# Variables dependent on Application basic functions
################################################################################

repo_root_path = os.path.dirname(os.getcwd())
appconfig = get_appconfig(repo_root_path)
SQLITE_FILENAME = os.path.join(repo_root_path, appconfig["url_dump"]["sqlite3_filename"])
AUTH_COOKIE_NAME = str(appconfig['application']["auth_cookie_name"])

# ZX: Trying a different approach
# keywords = {
#     "SQLITE_FILENAME" : appconfig["url_dump"]["sqlite3_filename"],
#     "AUTH_COOKIE_NAME" : str(appconfig['application']["auth_cookie_name"]),
# }
# const = lambda kw : keywords[kw]

################################################################################
# Constants
################################################################################

# SQLITE_FILENAME = appconfig["url_dump"]["sqlite3_filename"]
# AUTH_COOKIE_NAME = str(appconfig['application']["auth_cookie_name"])

################################################################################
# Classes
################################################################################

# N/A

################################################################################
# Functions
################################################################################

# N/A

def initialize_sqlite_db(sqlite_filename):
    """Initialize a sqlite3 database

    Table(s) created:

    1.  raw_url

    Args:
        N/A

    Returns:
        N/A
    """
    logging.info("[url_dump] - Ensuring existence of sqlite3 database [{0}]".format(sqlite_filename))
    # Create directory if not exists
    dirName = os.path.dirname(sqlite_filename)
    if not os.path.isdir(dirName):
        os.makedirs(dirName)
    #create_raw_url_tabl(sqlite_filename)

def create_parsed_url_table(sqlite_filename):
    """Initialize a sqlite3 database

    Tables created:

    1.  parsed_url

    Args:
        N/A

    Returns:
        N/A
    """
    # Create any tables that we might need here
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    with sqlite3.connect(sqlite_filename) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS parsed_url (
            hexdigest   text,
            scheme      text,
            netloc      text,
            path        text,
            params      text,
            query       text,
            fragment    text,
            count       integer,
            timestamp   text,
            status      integer,
            PRIMARY KEY (hexdigest)
            )''')


def process_raw_url(sqlite_filename):
    timestamp = datetime.utcnow()
    with sqlite3.connect(SQLITE_FILENAME) as conn:
        raw_url_cursor = conn.cursor()
        exec_cursor = conn.cursor()
        # res = cursor.execute(
        #     "INSERT OR REPLACE INTO raw_url (timestamp, url, status) VALUES (?, ?, ?)",
        #     (timestamp, url, status)
        # )

        # Fetch all at one go
        # cursor.execute("SELECT * FROM raw_url")
        # rec = cursor.fetchall()

        # Fetching one-by-one treating cursor as iterator
        for row in raw_url_cursor.execute("SELECT * FROM raw_url WHERE Status = 0"):
            print(row)

            # raw_url_cursor.execute("SELECT * FROM raw_url")
            # row = raw_url_cursor.fetchone()
            md5_hash = hashlib.md5(row[2]).hexdigest()
            parsed_res = urlparse(row[2])

            rowhex_count = 0
            exec_cursor.execute("SELECT * FROM parsed_url WHERE hexdigest = ?", (md5_hash,))
            rec = exec_cursor.fetchone()
            if rec is not None:
                rowhex_count = rec[7]
            rowhex_count = rowhex_count + 1
            res = exec_cursor.execute(
                "INSERT OR REPLACE INTO parsed_url (hexdigest, scheme, netloc, path, params, query, fragment, count, timestamp, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (md5_hash, parsed_res.scheme, parsed_res.netloc, parsed_res.path, parsed_res.params, parsed_res.query, parsed_res.fragment, rowhex_count, timestamp, 0)
                )
            res = exec_cursor.execute(
                "UPDATE raw_url SET status = 1 WHERE Id = ?",
                (row[0],)
                )


################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    logging.info("[PROGRAM START]")
    # logging.critical("%8s test message %s" % ("CRITICAL", str(datetime.utcnow())))
    # logging.error("%8s test message %s" % ("ERROR", str(datetime.utcnow())))
    # logging.warning("%8s test message %s" % ("WARNING", str(datetime.utcnow())))
    # logging.info("%8s test message %s" % ("INFO", str(datetime.utcnow())))
    # logging.debug("%8s test message %s" % ("DEBUG", str(datetime.utcnow())))

    # Parameters check    
    if not os.path.exists(SQLITE_FILENAME):
        logging.error("SQLITE does not exists at {0}".format(SQLITE_FILENAME))
        exit()
    create_parsed_url_table(SQLITE_FILENAME)

    # Initial modules that requires it
    # N/A
    
    # Do work here
    # ----------
    # timestamp = datetime.utcnow()
    # with sqlite3.connect(SQLITE_FILENAME) as conn:
    #     raw_url_cursor = conn.cursor()
    #     exec_cursor = conn.cursor()
    #     # res = cursor.execute(
    #     #     "INSERT OR REPLACE INTO raw_url (timestamp, url, status) VALUES (?, ?, ?)",
    #     #     (timestamp, url, status)
    #     # )

    #     # Fetch all at one go
    #     # cursor.execute("SELECT * FROM raw_url")
    #     # rec = cursor.fetchall()

    #     # Fetching one-by-one treating cursor as iterator
    #     for row in raw_url_cursor.execute("SELECT * FROM raw_url WHERE Status = 0"):
    #         print(row)

    #         # raw_url_cursor.execute("SELECT * FROM raw_url")
    #         # row = raw_url_cursor.fetchone()
    #         md5_hash = hashlib.md5(row[2]).hexdigest()
    #         parsed_res = urlparse(row[2])

    #         rowhex_count = 0
    #         exec_cursor.execute("SELECT * FROM parsed_url WHERE hexdigest = ?", (md5_hash,))
    #         rec = exec_cursor.fetchone()
    #         if rec is not None:
    #             rowhex_count = rec[7]
    #         rowhex_count = rowhex_count + 1
    #         res = exec_cursor.execute(
    #             "INSERT OR REPLACE INTO parsed_url (hexdigest, scheme, netloc, path, params, query, fragment, count, timestamp, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #             (md5_hash, parsed_res.scheme, parsed_res.netloc, parsed_res.path, parsed_res.params, parsed_res.query, parsed_res.fragment, rowhex_count, timestamp, 0)
    #             )
    #         res = exec_cursor.execute(
    #             "UPDATE raw_url SET status = 1 WHERE Id = ?",
    #             (row[0],)
    #             )

    # normalize do work to function
    process_raw_url(SQLITE_FILENAME)

    logging.info("[PROGRAM END]")

