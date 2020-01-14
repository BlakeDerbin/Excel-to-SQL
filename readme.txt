User Instructions

Before the program can be run the user must have the Anaconda IDE installed:
-	Download and install from: https://anaconda.org/anaconda/spyder
	-	Ensure that Python 3.7 version is the Anaconda IDE you download as the scripts as written in Python 3.7

If the Anaconda IDE is installed then:
-	Unzip the files into a new folder with a relevant name (i.e. Violations)
	-	All files must reside within the same folder in order for the scripts to work correctly

NOTE: The scripts must be run in the order stated in this section in order for the scripts to work correctly.

- 	Once all packages and installed open the application Spyder(Annaconda)
- 	When the application is loaded goto the "File" menu and select "Open"
	- 	Navigate to the folder where the files had been unzipped
		- 	Once in the folder open the file "createdb_food.py"
		- 	Once opened open the "run" menu and select "run"
			-	Then wait until the console outputs the final message "Data import complete."
			
-	Open the next file "sql_food.py" and run the script
	-	Wait until the console outputs the final message "Created table previous_violations and data import successful."
	
-	Open the next file "excel_food.py" and run the script
	-	Wait until the console outputs the final message "Excel ViolationsTypes.xlsx created sucessfully and data import complete."
	
-	Open the next file "numpy_food.py" and run the script
	-	Wait until the console outputs the final message "Graphs complete." and all graphs are loaded

- 	After the graphs have loaded and all scripts are run you may wish to exit the Anaconda IDE.

-	There will now be 2 new files created in the folder where you unzipped the scripts:
	- 	ViolationsTypes.xlsx: This will contain an excel spreadsheet with the total counts of violations that occured under each violation type in the dataset
	-	violations.db: This is the database file that has been created using the python scripts, this is an SQLite database and can be opened with a SQL database viewing program