# Module for project management
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
SQLITE_FILE_NAME = 'project_mgmt.sqlite3'
SQLITE_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, SQLITE_FILE_NAME)
constants = {
    DATA_DIRECTORY_PATH : './data/sqlite3',
    SQLITE_FILE_NAME : 'project_mgmt.sqlite3',
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

############################################################
# Sqlite3 related functions
############################################################

########################################
# lookup table functions
########################################


def create_lookup_table(sqlite3_cursor, table_name):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    """
    A generic lookup table has the following fields:
    ID
    NAME
    DESCRIPTION
    """
    return sqlite3_cursor.execute('''CREATE TABLE IF NOT EXISTS {0} (
        id                  integer,
        name                text,
        description         text,
        PRIMARY KEY (id)
        )'''.format(table_name))

def upsert_lookup(sqlite3_cursor, table_name, nd_list):
    for nd in nd_list:
        sqlite3_cursor.execute(
            "INSERT OR REPLACE INTO {0} (name, description) VALUES (?, ?)".format(table_name),
            (nd[0], nd[1])
            )

########################################
# isin table functions
########################################




########################################
# isin table functions
########################################

def create_project_table(sqlite3_cursor):
    # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
    """
    Project
    """
    return sqlite3_cursor.execute('''CREATE TABLE IF NOT EXISTS project (
        id                  integer, 
        name                text UNIQUE,
        category_id         integer,
        status_id           integer,
        timestamp           text,
        PRIMARY KEY (id)
        )''')

def upsert_project(sqlite3_cursor, name, category_id, status_id, timestamp):
    sqlite3_cursor.execute(
        "INSERT OR REPLACE INTO project (name, category_id, status_id, timestamp) VALUES (?, ?, ?, ?)",
        (name, category_id, status_id, timestamp)
        )


########################################
# create views
########################################

# def create_winner_summary_view(sqlite3_cursor):
#     # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
#     return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS winner_summary AS
# SELECT 	draw_number, draw_date,
# 		SUM(case when w.division = '1' then winner_count end) AS 'd1_cnt',
# 		SUM(case when w.division = '1' then prize end) AS 'd1_amt',
# 		SUM(case when w.division = '2' then winner_count end) AS 'd2_cnt',
# 		SUM(case when w.division = '2' then prize end) AS 'd2_amt',
# 		SUM(case when w.division = '3' then winner_count end) AS 'd3_cnt',
# 		SUM(case when w.division = '3' then prize end) AS 'd3_amt',
# 		SUM(case when w.division = '4' then winner_count end) AS 'd4_cnt',
# 		SUM(case when w.division = '4' then prize end) AS 'd4_amt',
# 		SUM(case when w.division = '5' then winner_count end) AS 'd5_cnt',
# 		SUM(case when w.division = '5' then prize end) AS 'd5_amt',
# 		SUM(case when w.division = '6' then winner_count end) AS 'd6_cnt',
# 		SUM(case when w.division = '6' then prize end) AS 'd6_amt',
# 		SUM(case when w.division = '7' then winner_count end) AS 'd7_cnt',
# 		SUM(case when w.division = '7' then prize end) AS 'd7_amt'
# FROM 	winner w
# GROUP BY 
# 		w.draw_number
# ORDER BY 
# 		w.draw_number DESC;
#         ''')

# def create_raw49_view(sqlite3_cursor):
#     # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
#     return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS raw49 AS
# SELECT 	* 
# FROM 	raw 
# WHERE 	draw_date >= '2014-10-17' 
# ORDER BY 
# 		draw_number DESC;
#         ''')

# def create_raw49_period_view(sqlite3_cursor):
#     # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
#     return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS raw49_period AS
# SELECT 	MIN(draw_date)	    AS 'min_draw_date', 
# 		MIN(draw_number)    AS 'min_draw_number', 
# 		MAX(draw_date)      AS 'max_draw_date', 
# 		MAX(draw_number)    AS 'max_draw_number'
# FROM 	raw49;
#         ''')

# def create_toto49_view(sqlite3_cursor):
#     # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
#     return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS toto49 AS
# SELECT 	r.draw_number
# 		, r.draw_date
# 		, r.num1
# 		, r.num2
# 		, r.num3
# 		, r.num4
# 		, r.num5
# 		, r.num6
# 		, r.num7
# 		, ws.d1_cnt
# 		, ws.d1_amt
# 		, ws.d2_cnt
# 		, ws.d2_amt
# 		, ws.d3_cnt
# 		, ws.d3_amt
# 		, ws.d4_cnt
# 		, ws.d4_amt
# 		, ws.d5_cnt
# 		, ws.d5_amt
# 		, ws.d6_cnt
# 		, ws.d6_amt
# 		, ws.d7_cnt
# 		, ws.d7_amt
# FROM 	raw r 
# INNER JOIN 
# 		winner_summary ws
# 		ON r.draw_number = ws.draw_number
# WHERE	r.draw_number >= 2998 
# ORDER BY 
# 		r.draw_number;
#         ''')


# def create_last_draw_view(sqlite3_cursor):
#     # ZX: Rememeber there are only 5 data types in Sqlite3: text, numeric, integer, real, blob
#     return sqlite3_cursor.execute('''CREATE VIEW IF NOT EXISTS last_draw AS
# SELECT 	* 
# FROM 	toto49 
# WHERE 	draw_number = (SELECT MAX(draw_number) FROM toto49);
#         ''')



########################################
# Query function(s)
########################################


def get_lookup(cursor, table_name):
    SQL_QUERY = """
    SELECT id, name, description FROM {0};
    """.format(table_name)
    cursor.execute(SQL_QUERY)
    result = cursor.fetchall()
    return result


# def get_last_draw():
#     SQL_QUERY = """
#     SELECT * FROM last_draw;
#     """
#     print(SQLITE_FILE_PATH)
#     with sqlite3.connect(SQLITE_FILE_PATH) as conn:
#         cursor = conn.cursor()
#         cursor.execute(SQL_QUERY)
#         result = cursor.fetchall()
#     return result


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
    """Initialize a sqlite3 database

    Table(s) created:
        N/A

    Args:
        N/A

    Returns:
        N/A
    """
    logging.info("Ensuring existence of sqlite3 database [{0}]".format(sqlitedb_path))
    with sqlite3.connect(sqlitedb_path) as conn:
        cursor = conn.cursor()
        create_lookup_table(cursor, "project_category")
        create_lookup_table(cursor, "project_status")
        create_project_table(cursor)

        # ZX:   Meant for one-time table init; but this function is intended to be called multiple times
        #       Doing manual process; KIV for now
        # upsert_lookup(cursor, "project_status", [
        #     ("Proposed", "A project that is only proposed; not started"),
        #     ("Ongoing", "An ongoing project"),
        #     ("Halt", "A project that has stopped or shelved"),
        #     ("Completed", "A completed project"),
        # ])
        # upsert_lookup(cursor, "project_category", [
        #     ("Game", "A game"),
        #     ("Trading", "A trading project"),
        #     ("Info", "A information scrapping project"),
        #     ("WebApp", "A web application"),
        # ])
        

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    initialize_sqlite_db(SQLITE_FILE_PATH)
