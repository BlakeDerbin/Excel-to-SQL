# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:04:34 2019

@author: Blake
"""

import sqlite3
import os, sys

prev_violations = []

# Checks if database file exists and if it does connects to database, else quits the script
def check_db_file():
    db_file = "./violations.db"
    # If file exists, run query
    if os.path.isfile(db_file):
        # Connecting to the database
        connection = sqlite3.connect("violations.db")
        cursor = connection.cursor()
        append_violations(cursor,connection)
        return cursor, connection
    # If file doesn't exist print error message
    else:
        print("Error: %s file not found" % db_file)
        sys.exit
        

def append_violations(cursor,connection):
    print("\nPrinting violations that are greater than one in descending order, please wait...\n")
    
    # Print query where violations are greater than one, sorted in descending order by the violations points count 
    cursor.execute("SELECT DISTINCT COUNT(violations.points), inspections.facility_name, facility_address, facility_zip, facility_city FROM inspections INNER JOIN violations on violations.serial_number = inspections.serial_number WHERE violations.points >= 1 GROUP BY facility_name ORDER BY COUNT(violations.points) DESC")
    result = cursor.fetchall()
    
    # Prints the first 2 values from the query, then stores the rest of the query after the second index to the prev_violations array
    for r in result:
        print(r[:2])
        prev_violations.append(r[1:])
    
    print("\nImporting facility violations data into table previous_violations, please wait....\n")
    check_table_exists(cursor,connection)

# Function that checks if the table exists and if it does it will drop the table then recreate it.
def check_table_exists(cursor, connection):
    try:
        # Creates new table previous violations with the facility name, address, zip and city cells
        cursor.execute("CREATE TABLE previous_violations (facility_name VARCHAR(500), facility_address VARCHAR(255), facility_zip VARCHAR(10), facility_city VARCHAR(255))")
        
        # Inserts the prev_violations array into the previous_violations table
        for v in prev_violations:
            cursor.execute('INSERT INTO previous_violations VALUES (?,?,?,?)', v)
           
        print("Created table previous_violations and data import successful.")
        
        # Commiting the database changes and closing the connection
        connection.commit()
        connection.close()
        
    except:
        print("The previos_violations table already exists, deleting table and creating again.\n")
        
        # Drops table 
        cursor.execute("DROP TABLE previous_violations")
        
        # Creates new table previous violations with the facility name, address, zip and city cells
        cursor.execute("CREATE TABLE previous_violations (facility_name VARCHAR(500), facility_address VARCHAR(255), facility_zip VARCHAR(10), facility_city VARCHAR(255))")
        
        # Inserts the prev_violations array into the previous_violations table
        for v in prev_violations:
            cursor.execute('INSERT INTO previous_violations VALUES (?,?,?,?)', v)
           
        print("Created table previous_violations and data import successful.")
        
        # Commiting the database changes and closing the connection
        connection.commit()
        connection.close()
        
check_db_file()