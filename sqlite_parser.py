#
# #############################################################################
# sqlite_parser to recover data from allocated and unallocated/slack db space
# python version: 2.7.6
# usage:
# version:
# ##############################################################################
#

#import necessary modules
#sys for  standard python library
#os for operating system and file I/O actions
#sqlite library to handle sqlite3 db
#import the Standard Library Module of handling program arguments
__author__ = 'aung'

import sys
import os
import struct
import argparse


#handle user inputs and process,pass it to main function
if __name__ == "__main__":
    args = parsecommandline()
    main(args.verbose,args.sqlDB,args.outPath)

#this function parse user input and optionals
def parsecommandline():
    parser = argparse.ArgumentParser('SQL DB Carving')
    parser.add_argument('-v', '--verbose', help="enables printing of additional program messages", action='store_true')
    parser.add_argument('-i', '--sqlDB',   type= ValidateFileRead,  required=True, help="input filename of the sqlite database")
    parser.add_argument('-o', '--outPath', type= ValidateDirectory, required=True, help="output path for extracted tables")

    theargs = parser.parse_args()
    return theargs
    
#main function
def main(verbose,sqldb,outpath):
    p = Display(verbose)
    p.print("Chrome Carving tool to recover the url records from browser ")

    ##check input file
    try:
        dbfile=open(sqldb,"rb")
    except:
        p.Print ("file not given...")
        exit(0)

    #filesize
    filesize = len(dbfile.read())
    p.print("file size:%s" %filesize)

    filesize.seek(0)

    #check sqlite file
    header = dbfile.read(16)

    if "SQLite" not in header:
        p.print ("File does not appear to be an SQLite File")
        exit(0)
    else:
        p.print ("Sqlite file found...")


    #get page size
    pagesize = struct.unpack('>H', dbfile.read(2))[0]

    offset = pagesize

    while offsize < filesize:



