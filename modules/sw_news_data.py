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


################################################################################
# CONSTANT(s)
################################################################################

DATA_DIRECTORY_PATH = './data/sqlite3'
SQLITE_FILE_NAME = 'sw-news.sqlite3'
SQLITE_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, SQLITE_FILE_NAME)
constants = {
    DATA_DIRECTORY_PATH : './data/sqlite3',
    SQLITE_FILE_NAME : 'sw-news.sqlite3',
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
# [software] table functions
########################################

def create_software_table(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    return sqlite3_cursor.execute('''CREATE TABLE IF NOT EXISTS software (
        name            text,
        version         text,
        last_updated    text,
        md5             text,
        last_checked    text,
        last_md5        text,
        status          integer,
        PRIMARY KEY (name)
        )''')

def add_software_news(sqlite3_cursor, name, version, last_updated, md5, last_checked):
    return sqlite3_cursor.execute(
        "INSERT OR REPLACE INTO software (name, version, last_updated, md5, last_checked, last_md5) VALUES (?, ?, ?, ?, ?, ?)",
        (name, version, last_updated, None, last_checked, None)
    )

# def add_news(json_data):
#     with sqlite3.connect(SQLITE_FILE_PATH) as conn:
#         cursor = conn.cursor()
#         #
#         # {'name': 'nodejs (current)', 
#         # 'version': 'v11.9.0', 
#         # 'last_updated': None, 
#         # 'last_checked': '2019-02-09', 
#         # 'md5_hash': '18d49f20ff1b1c2aa5959b1ba46ee104'}
#         upsert_software(
#             cursor, 
#             json_data['name'],
#             json_data['version'],
#             json_data['last_updated'],
#             json_data['last_checked']
#         )  
#     # return result
#     # # with sqlite3.connect(SQLITE_FILE_PATH) as conn:
#     # #     cursor = conn.cursor()
#     # #     for row in csv_reader:
#     # #         #results.append(row)
#     # #         exec_cursor = add_raw(
#     # #             cursor, 
#     # #             row[0], # draw_number
#     # #             row[1], # draw_date
#     # #             row[2], # num1
#     # #             row[3], # num2
#     # #             row[4], # num3
#     # #             row[5], # num4
#     # #             row[6], # num5
#     # #             row[7], # num6
#     # #             row[8], # num7
#     # #             ''      # remarks
#     # #             )
#         "INSERT INTO software (name, version, last_updated, md5, last_checked, last_md5, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
#         (name, version, last_updated, md5, last_checked, None, 0)
#     )

def update_software_last_checked(sqlite3_cursor, name, last_checked):
    return sqlite3_cursor.execute(
        """
        UPDATE  software 
        SET     last_checked    = ?
        WHERE   name = ?
        """,
        (last_checked, name)
    )


def update_software(sqlite3_cursor, name, version, last_updated, md5, last_checked, last_md5, status):
    return sqlite3_cursor.execute(
        """
        UPDATE  software 
        SET     version         = ?, 
                last_updated    = ?, 
                md5             = ?,
                last_checked    = ?, 
                last_md5        = ?, 
                status          = ?
        WHERE   name = ?
        """,
        (version, last_updated, md5, last_checked, last_md5, status, name)
    )


def update_software_news(name, version, last_updated, md5, last_checked):
    
    logging.debug("update_software_news")
    
    # Algorithm
    # ---------
    # If record does not exists, add record to table
    # If record exists, update last_updated date ONLY   if md5 is the same.
    # If record exists, update record                   if md5 is different.

    with sqlite3.connect(SQLITE_FILE_PATH) as conn:
        cursor = conn.cursor()
        record_list = get_software(cursor, name)

        if len(record_list) <= 0: # If record does not exists
            # add record to table
            add_software_news(cursor, name, version, last_updated, md5, last_checked)
        else: # If record exists
            rec = record_list[0]
            last_md5 = rec[3] 

            if md5 == last_md5: # if md5 is the same.
                # update last_updated date ONLY
                update_software_last_checked(cursor, name, last_checked)
            else:
                # update record
                update_software(cursor, name, version, last_updated, md5, last_checked, last_md5, 1)


########################################
# create views
########################################

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

####################
# Dependent queries
####################

def get_software(sqlite3_cursor, name):
    SQL_QUERY = """
    SELECT * FROM software WHERE name = ?;
    """
    sqlite3_cursor.execute(
        SQL_QUERY,
        (name,)
    )
    result = sqlite3_cursor.fetchall()
    return result

####################
# Standalone queries
####################

def get_software_list():
    SQL_QUERY = """
    SELECT name, version, last_checked FROM software;
    """
    #print(SQLITE_FILE_PATH)
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
    """Initialize a sqlite3 database for tracking software new.

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
        create_software_table(cursor)
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
    initialize_sqlite_db(SQLITE_FILE_NAME)
