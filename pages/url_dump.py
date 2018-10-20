################################################################################
# Modules and functions import statements
################################################################################

import logging
import pdb
import sqlite3

from helpers.app_helpers import *
from helpers.page_helpers import *
from helpers.jinja2_helpers import *

################################################################################
# Setup helper functions
################################################################################

# N/A

def init():
    logging.debug("Init url_dump pages module")
    sqlite_filename = appconfig["url_dump"]["sqlite3_filename"]
    initialize_sqlite_db(sqlite_filename)

################################################################################
# Sqlite3 functions
################################################################################

def initialize_sqlite_db(sqlite_filename):
    """Initialize a sqlite3 database

    Table(s) created:

    1.  raw_url

    Args:
        N/A

    Returns:
        N/A
    """
    logging.info("Ensuring existence of sqlite3 database [{0}]".format(sqlite_filename))
    # Create any tables that we might need here
    create_raw_url_tabl(sqlite_filename)
    


########################################
# Table(s) creation
########################################

def create_raw_url_tabl(sqlite_filename):
    """Initialize a sqlite3 database

    Tables created:

    1.  raw_url

    Args:
        N/A

    Returns:
        N/A
    """
    # Create any tables that we might need here
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    with sqlite3.connect(sqlite_filename) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS raw_url (
            timestamp   text,
            url         text,
            status      integer
            )''')

########################################
# DML
########################################

def add_raw_url(sqlite_filename, timestamp, url_list, status):
    count = 0
    with sqlite3.connect(sqlite_filename) as conn:
        cursor = conn.cursor()
        for url in url_list:
            res = cursor.execute(
                "INSERT OR REPLACE INTO raw_url (timestamp, url, status) VALUES (?, ?, ?)",
                (timestamp, url, status)
            )
            if res.lastrowid != None:
                count = count + 1
    return count

################################################################################
# Setup commonly used routes
################################################################################

@route('/url_dump', method=['POST','GET'])
def display_home_page(errorMessages=None):
    #logging.debug("IN display_home_page")
    context = get_default_context(request)

    if request.method == 'POST':
        #logging.debug("IN POST block")

        # Handle saving of text
        if 'save_text_textarea' in request.forms.keys():
            # Save text here
            url_list = []
            for line in request.forms['save_text_textarea'].split("\n"):
                line = line.strip()
                if line != "":
                    url_list.append(line)

            sqlite_filename = appconfig["url_dump"]["sqlite3_filename"]
            rows_affected = add_raw_url(sqlite_filename, datetime.utcnow(), url_list, 0)
            if rows_affected > 0:
                context["notification"] = "%d record(s) saved." % rows_affected

        # Handle saving of file
        if 'upload_file' in request.files:
            logging.debug("[upload_file] key exists in request.files")
            upload_file = request.files['upload_file']
            logging.debug(str(dir(upload_file)))
            upload_file.save("./data/" + upload_file.filename)
            logging.debug("Saving [upload_file]")
        
    return jinja2_env.get_template('html/url_dump/home-page.html').render(context)

# @route('/url_dump/upload', method=['POST','GET'])
# def upload_url_list(errorMessages=None):
#     logging.debug("IN upload_url_list")

#     if request.method == 'POST':
#         logging.debug("IN POST block")
#         if 'upload_file' in request.files:
#             logging.debug("[upload_file] key exists in request.files")
#             upload_file = request.files['upload_file']
#             logging.debug(str(dir(upload_file)))
#             upload_file.save("./data/" + upload_file.filename)
#             logging.debug("Saving [upload_file]")
#             #return 'file uploaded successfully'
    
    
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/url_dump/home-page.html').render(context)


# @route('/url_dump/save-text', method=['POST', 'GET'])
# def upload_url_list(errorMessages=None):
#     logging.debug("IN upload_url_list")

#     if request.method == 'POST':
#         logging.debug("IN POST block")
#         if 'save_text_textarea' in request.forms.keys():
#             # Save text here
#             import pdb
#             pdb.set_trace()
#             redirect('/url_dump#save-text')
#             pass
    
#     context = get_default_context(request)
#     return jinja2_env.get_template('html/url_dump/home-page.html').render(context)