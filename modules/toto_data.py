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

DATA_DIRECTORY_PATH = './data/csv'
SQLITE_FILE_NAME = 'toto-2018.sqlite3'
SQLITE_FILE_PATH = os.path.join(DATA_DIRECTORY_PATH, SQLITE_FILE_NAME)
constants = {
    DATA_DIRECTORY_PATH : './data/csv',
    SQLITE_FILE_NAME : 'toto-2018.sqlite3',
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
        create_raw_table(cursor)
        create_winner_table(cursor)
        create_winner_summary_view(cursor)
        create_raw49_view(cursor)
        create_raw49_period_view(cursor)
        create_toto49_view(cursor)
        create_last_draw_view(cursor)
        

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    initialize_sqlite_db(SQLITE_FILE_NAME)
