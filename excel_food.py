# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 09:11:28 2019

@author: Blake
"""

from openpyxl.styles import Font
import openpyxl
import sqlite3
import os, sys

# Checks if database file exists and if it does connects to database, else quits the script
# Checks if excel file exists, if it does it deletes the file
def check_db_file():
    db_file = "./violations.db"
    excel_file = "./ViolationsTypes.xlsx"
    # If file exists, run query
    if os.path.isfile(db_file):
        if os.path.isfile(excel_file):
            # Removes excel file if it exists
            print("ViolationsTypes.xlsx found, deleting file.")
            os.remove(excel_file)
            
            # Connecting to the database
            connection = sqlite3.connect("violations.db")
            cursor = connection.cursor()
            append_data(cursor,connection)
            return cursor, connection
        
        else:
            # Connecting to the database
            connection = sqlite3.connect("violations.db")
            cursor = connection.cursor()
            append_data(cursor,connection)
            return cursor, connection
        
    # If file doesn't exist print error message
    else:
        print("Error: %s file not found" % db_file)
        sys.exit
        

def append_data(cursor,connection):
    print("Creating excel file ViolationsTypes.xlsx and importing data.")
    
    # Creating a workbook and setting the sheet name
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Violations Types"
    
    # Connecting to the database
    connection = sqlite3.connect("violations.db")
    cursor = connection.cursor()
    
    # SQL Query
    cursor.execute("SELECT DISTINCT violation_code, violation_description, COUNT(violation_code) FROM violations GROUP BY violation_code")
    
    # Fetching all query results
    result = cursor.fetchall()
    
    violation_data = []
    
    # Using a for loop to get a count of each violation code
    for r in result:
        violation_data.append(r)
    
    # Setting the first values in the columns A to C to be in bold font
    sheet["A1"].font = Font(bold=True)
    sheet["B1"].font = Font(bold=True)
    sheet["C1"].font = Font(bold=True)
    
    # Setting the first values of the columns A to C 
    sheet["A1"] = "Code" 
    sheet["B1"] = "Description"
    sheet["C1"] = "Count"
    
    # Using a for loop to append the data to the excel sheet
    for data in violation_data:
        sheet.append(data)
    
    # Calculating the total violations
    sheet["B118"] = "Total Violations"
    sheet["C118"] = "=SUM(C2:C117)"
    
    # Saving the workbook changes and name
    wb.save(filename="ViolationsTypes.xlsx")
    
    print("Excel ViolationsTypes.xlsx created sucessfully and data import complete.")
    
check_db_file()