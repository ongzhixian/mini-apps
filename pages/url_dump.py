################################################################################
# Modules and functions import statements
################################################################################

import logging
import pdb
import sqlite3
import tempfile

from helpers.app_helpers import *
from helpers.page_helpers import *
from helpers.jinja2_helpers import *

################################################################################
# Constants
################################################################################

SQLITE_FILENAME = appconfig["url_dump"]["sqlite3_filename"]
AUTH_COOKIE_NAME = str(appconfig['application']["auth_cookie_name"])

################################################################################
# Setup helper functions
################################################################################

# N/A

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
    logging.info("[url_dump] - Ensuring existence of sqlite3 database [{0}]".format(sqlite_filename))
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
            id          integer,
            timestamp   text,
            url         text,
            status      integer,
            PRIMARY KEY (id)
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


def save_url_list(url_list):
    rows_affected = add_raw_url(SQLITE_FILENAME, datetime.utcnow(), url_list, 0)
    return rows_affected


def make_url_list(raw_lines):
    url_list = []
    for line in raw_lines:
        line = line.strip()
        if line != "":
            url_list.append(line)
    return url_list

################################################################################
# Setup commonly used routes
################################################################################

@route('/url-dump', method=['POST','GET'])
def display_home_page(errorMessages=None):
    #logging.debug("IN display_home_page")
    context = get_default_context(request)

    if request.method == 'POST':
        #logging.debug("IN POST block")

        # Handle saving of text
        if 'save_text_textarea' in request.forms.keys():
            # Process text into array of urls
            url_list = make_url_list(request.forms['save_text_textarea'].split("\n"))
            
        # Handle saving of file
        if 'upload_file_input' in request.files:
            # Saving upload of files
            upload_file = request.files['upload_file_input']
            
            # If cookie is NOT in request, generate cookie
            if AUTH_COOKIE_NAME not in request.cookies:
                cookie_value = add_auth_cookie(AUTH_COOKIE_NAME)
            else:
                cookie_value = request.cookies[AUTH_COOKIE_NAME]

            # Save contents to a temporary file, and process the temp file.
            with tempfile.TemporaryFile() as temp_file:
                # Read contents of the upload file and save dump it into temp file
                upload_file_content = upload_file.file.read()
                temp_file.write(upload_file_content)
                temp_file.flush()

                # Reset the file point to the beginning of the file to read from beginning
                temp_file.seek(0)
                temp_file_lines = temp_file.readlines()

                url_list = make_url_list(temp_file_lines)

        # Save url list
        if len(url_list) > 0:
            rows_affected = save_url_list(url_list)
            if rows_affected > 0:
                context["notification"] = "%d record(s) saved." % rows_affected
        
    return jinja2_env.get_template('html/url_dump/home-page.html').render(context)

################################################################################
# Module initialization
################################################################################

initialize_sqlite_db(SQLITE_FILENAME)