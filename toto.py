# Python application to watch for changes within file system.
################################################################################
# Import statements
################################################################################

import json
import logging
from datetime import datetime

################################################################################
# Setup logging configuration
################################################################################

logging_format = '%(asctime)-15s %(levelname)-8s %(message)s'
#logging_format = '%(asctime)-15s %(levelname)-8s %(module)-16s %(funcName)-24s %(message)s'
logging.basicConfig(filename='watch.log', level=logging.DEBUG, format=logging_format) # Log to file
console_logger = logging.StreamHandler() # Log to console as well
console_logger.setFormatter(logging.Formatter(logging_format))
logging.getLogger().addHandler(console_logger)

################################################################################
# Import helper modules
################################################################################

from helpers import *

################################################################################
# Setup appconfig
################################################################################

appconfig = app_helpers.appconfig

################################################################################
# Import api modules
################################################################################

#from api import *

################################################################################
# Import pages modules
################################################################################

#from pages import *

################################################################################
# Functions
################################################################################

def initialize_sqlite_db(sqlite_filename):
    """Initialize a sqlite3 database for tracking ASX sector indices.

    Table(s) created:

    1.  sector_indices

    Args:
        N/A

    Returns:
        N/A
    """
    logging.info("Ensuring existence of sqlite3 database [{0}]".format(sqlite_filename))

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    logging.info("[PROGRAM START]")
    logging.critical("%8s test message %s" % ("CRITICAL", str(datetime.utcnow())))
    logging.error("%8s test message %s" % ("ERROR", str(datetime.utcnow())))
    logging.warning("%8s test message %s" % ("WARNING", str(datetime.utcnow())))
    logging.info("%8s test message %s" % ("INFO", str(datetime.utcnow())))
    logging.debug("%8s test message %s" % ("DEBUG", str(datetime.utcnow())))
    # Initial modules that requires it

    #from os import path
    from modules import toto_data
    toto_data.init()
    #toto_data.load_csv('./data/csv/toto-2018.csv')
    toto_data.csv_to_db('./data/csv/toto-2018.csv')
    
    

    # import os
    
    # data_directoryPath = './data/csv'
    # sqlite_fileName = 'toto-2018.sqlite3'
    # sqlite_filePath = os.path.join(data_directoryPath, sqlite_fileName)
    #sqlite_filename = './data/csv/toto-2018.sqlite3'

    # Read a csv file and dump contents into a Sqlite3 database.
    # import sqlite3
    # import csv

    # with open('./data/csv/toto-2018.csv', 'rb') as csvfile:
    #     csv_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    #     # csv_reader.next() # Use next() to rows such as headers.
    #     for row in csv_reader:
    #         print(row)

    # with sqlite3.connect(sqlite_filePath) as conn:
    #     cursor = conn.cursor()
    #     # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    #     cursor.execute('''CREATE TABLE IF NOT EXISTS raw (
    #         draw_number         numeric ,
    #         draw_date           text,
    #         num1                numeric,
    #         num2                numeric,
    #         num3                numeric,
    #         num4                numeric,
    #         num5                numeric,
    #         num6                numeric,
    #         num7                numeric,
    #         remarks             text,
    #         PRIMARY KEY (draw_number)
    #         )''')
    
    
    logging.info("[PROGRAM END]")

