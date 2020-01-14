# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 08:45:53 2019

@author: Blake
"""

import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os, sys

temp_array = []
violations = []
violationsReverse = []
violationsCA = []
violationsMcD = []
violationsBking = []

# Setting a date range to use for the plotting of graphs
datesRange = np.arange('2015-07', '2018-01', dtype='datetime64[M]')

# Checks if database file exists and if it does connects to database, else quits the script
def check_db_file():
    db_file = "./violations.db"
    # If file exists, run query
    if os.path.isfile(db_file):
        # creates a connection to sqlite database and returns cursor
        connection = sqlite3.connect("violations.db")
        cursor = connection.cursor()
        main_function(cursor)
        return cursor, connection
    # If file doesn't exist print error message
    else:
        print("Error: %s file not found" % db_file)
        sys.exit


# executes the main portion of the program
def main_function(cursor):
    # executes query and fetches all results, returns results as temp_variable
    def query_db_result(cursor, query):
        cursor.execute(query)
        temp_variable = cursor.fetchall()
        return temp_variable
    
    print('Storing data from database, please wait...')
    
    # Query that Selects the date as year and month, removes the +4 digits from the facility_zip, 
    # selects the facility_state, gets the sum of vioaltions.points
    # sorts the result based by year-month and zip code, orders it by year_month and highest sum of violation points
    raw_v = query_db_result(cursor, '''SELECT DISTINCT
                   strftime('%Y-%m', activity_date) AS year_month,
                   (CAST(REPLACE(CAST(facility_zip AS VARCHAR(5)), '', '') AS INT)) as facility_zip,
                   facility_state,
                   SUM(violations.points) AS violation_sum
                   FROM inspections 
                   INNER JOIN violations on violations.serial_number = inspections.serial_number 
                   GROUP BY year_month, (CAST(REPLACE(CAST(facility_zip AS VARCHAR(5)), '', '') AS INT))
                   ORDER BY year_month, violation_sum DESC
                   ''')
    
    # converts the array into a numpy array
    violations = np.array(raw_v, dtype={'names':('year_month', 'zip','state', 'violations'),
                                             'formats':('datetime64[M]', 'U10', 'U10', 'i4')})
        
     
    #reverses list to get minimum value first
    violationsReverse = violations[::-1]
    
    # Query that Selects the date as year and month, counts the violation points as a sum, Counts the distinct times a zip code appears in query,
    # Average is caluculated by dividing the sum of violation.points by the count of zip codes
    # Grouped by year_month and ordered by year_month   
    raw_vAVG = query_db_result(cursor, '''SELECT DISTINCT
                   strftime('%Y-%m', activity_date) AS year_month,
                   SUM(violations.points) AS violation_sum,
    			   COUNT(DISTINCT (CAST(REPLACE(CAST(facility_zip AS VARCHAR(5)), '', '') AS INT))) as zip_count,
    			   SUM(violations.points)/COUNT(DISTINCT (CAST(REPLACE(CAST(facility_zip AS VARCHAR(5)), '', '') AS INT))) as monthly_average
                   FROM inspections 
                   INNER JOIN violations on violations.serial_number = inspections.serial_number
                   GROUP BY year_month
                   ORDER BY year_month''')
    
    # converts the array into a numpy array
    violationsCA =  np.array(raw_vAVG, dtype={'names':('year_month', 'violation_sum', 'zip_count', 'monthly_average'),
                                             'formats':('datetime64[M]', 'i4', 'i4', 'i4')})
    
    # # Query that Selects the date as year and month, counts the violation points as a sum, Counts the distinct times a facility_name appears in query,
    # Average is caluculated by dividing the sum of violation.points by the count of distinct facility_name
    # the facility name is then only counted where it contains "MCDONALD" in the first 
    # Grouped by year_month and ordered by year_month
    raw_vMcD = query_db_result(cursor, '''SELECT DISTINCT
                   strftime('%Y-%m', activity_date) AS year_month,
                   SUM(violations.points) AS violation_sum,
    			   COUNT(DISTINCT facility_name) AS facility_count,
    			   SUM(violations.points)/COUNT(DISTINCT facility_name) as monthly_average
                   FROM inspections 
                   INNER JOIN violations on violations.serial_number = inspections.serial_number 
    			   WHERE facility_name LIKE 'MCDONALD%'
                   GROUP BY year_month
                   ORDER BY year_month''')
    
    # converts the array into a numpy array
    violationsMcD =  np.array(raw_vMcD, dtype={'names':('year_month', 'violation_sum', 'facility_count', 'monthly_average'),
                                             'formats':('datetime64[M]', 'i4', 'i4', 'i4')})
    
    # # Query that Selects the date as year and month, counts the violation points as a sum, Counts the distinct times a facility_name appears in query,
    # Average is caluculated by dividing the sum of violation.points by the count of distinct facility_name
    # the facility name is then only counted where it contains "BURGER KING" in the first 
    # Grouped by year_month and ordered by year_month
    raw_vBking = query_db_result(cursor, '''SELECT DISTINCT
                   strftime('%Y-%m', activity_date) AS year_month,
                   sum(violations.points) AS violation_sum,
    			   COUNT(DISTINCT facility_name) AS facility_count,
    			   sum(violations.points)/count(DISTINCT facility_name) as monthly_average
                   FROM inspections 
                   INNER JOIN violations on violations.serial_number = inspections.serial_number 
    			   WHERE facility_name LIKE 'BURGER KING%'
                   GROUP BY year_month
                   ORDER BY year_month''')
    
    # converts the array into a numpy array
    violationsBking =  np.array(raw_vBking, dtype={'names':('year_month', 'violation_sum', 'facility_count', 'monthly_average'),
                                             'formats':('datetime64[M]', 'i4', 'i4', 'i4')})
    
    print('Data stored, plotting graphs please wait...')
    
    # returns the first row from violations where the input is matched with the date in the array violations
    def violation_strip(i, violation_list):
        for v in violation_list:
            if v[0] == i:
                return v
    
    violationsMax = []
    violationsMin = [] 
    
    # steps through each month using np.arange and appends the results from violation_strip to a list
    for d in datesRange:
        violationsMax.append(violation_strip(d,violations))
        violationsMin.append(violation_strip(d,violationsReverse))
        
    #print(violationsMin, "\n")
    #print(violationsMax, "\n")
    #print(violationsMcD, "\n")
    #print(violationsBking, "\n")
    #print(violationsCA, "\n")
    
    # converts the array into a numpy array    
    violationsMin = np.array(violationsMin, dtype={'names':('year_month', 'zip','state', 'violations'),
                                             'formats':('datetime64[M]', 'U10', 'U10', 'i4')})
        
    violationsMax = np.array(violationsMax, dtype={'names':('year_month', 'zip','state', 'violations'),
                                             'formats':('datetime64[M]', 'U10', 'U10', 'i4')})
    
    
    #Plot for postcode with most violations per month
    plt.figure(1)
    plt.plot(datesRange, violationsMax['violations'] )
    plt.xlabel('Months')
    plt.ylabel('Violations')
    plt.title('Highest zip code violations per month')
    
    #plot for postcode with least violations per month
    plt.figure(2)
    plt.plot(datesRange, violationsMin['violations'] )
    plt.xlabel('Months')
    plt.ylabel('Violations')
    plt.title('Lowest zip code violations per month')
    
    #plot for the average violations in the state of california
    plt.figure(3)
    plt.plot(datesRange, violationsCA['monthly_average'] )
    plt.xlabel('Months')
    plt.ylabel('Violations')
    plt.title('Average violations in California per month')
    
    #plots the average violations per month for mcdonalds and burgerking
    plt.figure(4)
    plt.plot(datesRange, violationsMcD['monthly_average'], 'r', datesRange, violationsBking['monthly_average'], 'b')
    plt.xlabel('Months')
    plt.ylabel('Violations')
    plt.title('Average violations per month of McDonalds and Burger King')
    
    plt.show()
    
    print("Graphs complete.")
    
check_db_file()