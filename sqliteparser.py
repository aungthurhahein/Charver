#
# Python Forensics
#
# SQLite Part I: Basic SQL Database Dump
#
# Dumps the table names and contents of each table
# by creating a Comma Separated Value (CSV) with the contents
# of each table
#
# Sample code with detailed comments.  
#
# usage: python sqlitePartOne.py -v -i .\main.db .\result
#
# Python Version 2.7.x
#
# Version 1.1  June 30, 2014
#

'''
Copyright (c) 2014 Chet Hosmer, Python Forensics, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

'''

# Import the standard library module sqlite3
# This type of import allows you to abbreviate the interface
# to sql methods.   i.e. sql.connect  vs sqlite3.connect
import sqlite3 as sql

# import the system module from the standard library
import sys

# import the standard library csv to handle comma separated value file I/O
import csv

# import the Operating System Module this handles file system I/O operations and definitions
import os

# import the Standard Library Module of handling program arguments
import argparse

#=====================================================================
#
# Local Classes and Method Definitions
#
#=====================================================================

# 
# Class: CSVWriter 
#
# Desc: Handles all methods related to comma separated value operations
#
# Methods  constructor:    Initializes the CSV File and writes the header row supplied (as a List)
#          writeCVSRow:    Writes a single row to the csv file
#          destructor:     Closes the CSV File

class CSVWriter:

    def __init__(self, csvFile, heading):
        try:
            # create a writer object and then write the header row
            self.csvFile = open(csvFile, 'w')
            self.writer = csv.writer(self.csvFile, delimiter=',',quoting=csv.QUOTE_ALL)
            self.writer.writerow(heading)
        except:
            print "CSV File: Initialization Failed"
            sys.exit(1)

    def writeCSVRow(self, row):
        try:
            rowList = []
            for item in row:

                if type(item) == unicode or type(item) == str:
                    item = item.encode('ascii','ignore')

                rowList.append(item)

            self.writer.writerow(rowList)

        except:
            print "CSV File Write: Failed" 
            sys.exit(1)

    def __del__(self):
        # Close the CSV File
        try:
            self.csvFile.close()
        except:
            print "Failed to close CSV File Object"
            sys.exit(1)

# End CSV Writer Class ====================================

#
# Display Class
# Replaces basic print function with two advantages
# 1. It will only print to the console if verbose was selected by the user
# 2. It will work with both Python 2.x and 3.x printing 
#

class Display():

    def __init__(self, verbose):
        self.verbose = verbose
        self.ver = sys.version_info

    def Print(self, msg):
        if self.verbose:

            if self.ver >= (3,0):
                print(msg)
            else:
                print msg        

# Display CLASS

# Name: ParseCommand() Function
#
# Desc: Process and Validate the command line arguments
#           use Python Standard Library module argparse
#
# Input: none
#  
# Actions: 
#              Uses the standard library argparse to process the command line
#
# For this program we expect 3 potential arguments
# -v which asks the program to provide verbose output
# -i which defines the full path and file name of the sqlite database to dump
# -d which defines the directory where the resulting table dumps should be stored
#
def ParseCommandLine():

    parser = argparse.ArgumentParser('SQL DB Dump')

    parser.add_argument('-v', '--verbose', help="enables printing of additional program messages", action='store_true')
    parser.add_argument('-i', '--sqlDB',   type= ValidateFileRead,  required=True, help="input filename of the sqlite database")
    parser.add_argument('-o', '--outPath', type= ValidateDirectory, required=True, help="output path for extracted tables")    

    theArgs = parser.parse_args()           

    return theArgs

# End ParseCommandLine()

#
# Name: ValidateFileRead Function
#
# Desc: Function that will validate that a file exists and is readable
#
# Input: A file name with full path
#  
# Actions: 
#              if valid will return path
#
#              if invalid it will raise an ArgumentTypeError within argparse
#              which will inturn be reported by argparse to the user
#

def ValidateFileRead(theFile):

    # Validate the path is a valid
    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File does not exist')

    # Validate the path is readable
    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File is not readable')

# End ValidateFileRead()

#
# Name: ValidateDirectory Function
#
# Desc: Function that will validate that the directory exists and is writable
#
# Input: Path to a Directory 
#  
# Actions: 
#              if valid will return path
#
#              if invalid it will raise an ArgumentTypeError within argparse
#              which will inturn be reported by argparse to the user
#

def ValidateDirectory(theDirectory):

    # Validate the path is a valid directory
    if not os.path.exists(theDirectory):
        raise argparse.ArgumentTypeError('Directory does not exist')

    # Validate the path is writable
    if os.access(theDirectory, os.W_OK):
        return theDirectory
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')

# End ValidateDirectory()

#=====================================================================
# Main Function Starts Here
#=====================================================================

# Main program for SQL Dump
# 
# Input: 
#       verboseFlag: used to be loud or silent in processing
#       theDB:       full path and filename of the input sqlite database file
#       outPath:     the path of the designated results directory

def main(verboseFlag, theDB, outPath):

    p = Display(verboseFlag)
    p.Print("Python Forensics: SQLite Investigation Part One - Simple Database Dump")

    try:
        # attempt to connect to a database file
        # this example uses the skype main.db that I have copied into
        # my local directory for easy access

        db = None
        db = sql.connect(theDB)

        # sql requires a cursor 
        # A database cursor is a  structure that enables you traverse over the records in a database
        # Cursors facilitate operations such as retrieval, addition and deletion of records contained
        # in a database

        dbCursor = db.cursor()    

        # Now let's utilize the cursor to execute a simple SQL command
        # that extracts the table names from the database

        dbCursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # The next statement fetches all the results from the table query

        tableTuple = dbCursor.fetchall()

        # For good measure let's print the list of tables
        # associated with this datbase

        p.Print("Tables Found")

        for table in tableTuple:
            p.Print(table[0])

        # Now we have all the table names in the object tableTuple
        # We can interate through each tuple entry

        for item in tableTuple:

            # For this particular tuple we are only interested in the first
            # entry which is the name of the table

            tableName = item[0]
            p.Print("Processing Table: "+tableName+"\n")

            # Now we can use the table name to extract data
            # contained in the table

            tableQuery = "SELECT * FROM "+tableName 

            # We will use the cursor to execute the query
            # and then collect the row data using the fetchall() method

            dbCursor.execute(tableQuery)

            # Obtain the table description
            tableDescription = dbCursor.description      

            # Create a heading for each table
            tableHeading = []
            for item in tableDescription:
                tableHeading.append(item[0])

            oCSV = CSVWriter(outPath+os.sep+tableName+'.csv', tableHeading)

            rowData = dbCursor.fetchall()

            # Now we can interate through the row data
            # and write the results to the associated CSV file

            for row in rowData:
                oCSV.writeCSVRow(row)

            oCSV.__del__()

    except:
        p.Print ("SQL Error")
        sys.exit(1)

    finally:

        if db:
            db.close()    

    p.Print("End Program")

# End Main program

#=================================================================
# Main Program Entry Point
#=================================================================

# Processes the user supplied arguments
# and if successful calls the main function
# with the appropriate arguments

if __name__ == "__main__":

    args = ParseCommandLine()

    # Call main passing the user defined arguments

    main(args.verbose, args.sqlDB, args.outPath)