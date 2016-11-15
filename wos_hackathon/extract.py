#!/usr/bin/env python
# coding: utf-8
import argparse
#import mysql.connector
import logging
import xml.etree.cElementTree as ET
import sys
import json
import csv
log_levels = { "DEBUG"   : logging.DEBUG,
               "INFO"    : logging.INFO,
               "WARNING" : logging.WARNING,
               "ERROR"   : logging.ERROR,
               "CRITICAL": logging.CRITICAL
}
import sys
import csv
maxInt = sys.maxsize

def get_data(filename, tablename, headers=None, delimiter='|', header_alternate={}, translator={}, kind=None):
    try :
        f = open(filename, 'rb')
        f_handle = open(tablename + '.sql', 'w')
        count = 1
        if headers == "implicit":
            headers = f.readline().strip().split(delimiter)
            print headers
            f_handle.write("INSERT IGNORE INTO {0} ({1})\n".format(tablename, ', '.join(headers)))
            f_handle.write("VALUES\n")
            f.next()
            for line in f:
                count += 1
                items = line.strip().split(delimiter)
                f_handle.write('\n(')
                f_handle.write(','.join([json.dumps(i) for i in items]))
                f_handle.write('),') 
                if count % 1000 == 0 :
                    f_handle.seek(-1, 1)
                    f_handle.write(';\n\n')
                    f_handle.write("INSERT IGNORE INTO {0} ({1})\n".format(tablename, ', '.join(headers)))
                    f_handle.write("VALUES\n")

                    

            
    except Exception, e:
        print "[ERROR]Caught exception in opening the file:{0}".format(filename)
        print "[ERROR]Reason : {0}".format(e)
        exit(-1)

    f_handle.close()
    f.close()
    return 
    #return list(reader)
    
# From stackoverflow
# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, count):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), count):
        yield l[i:i+count]

def dump(data, header, sql_header, table_name, file_name):
    chunksize = 1000
    
    print  "Writing out {0} to {1}".format(table_name, file_name)
    with open(file_name, 'w') as f_handle:
        
        #f_handle.write(sql_header.format(table_name))
        f_handle.write('\n')
        for chunk in chunks(data, 1000):
            f_handle.write("INSERT IGNORE INTO {0} ({1})\n".format(table_name, ', '.join(header)))
            f_handle.write("VALUES\n")

            for row in chunk :
                f_handle.write('\n(')
                f_handle.write(','.join([json.dumps(row.get(attr, 'NULL')) for attr in header]))
                f_handle.write('),')            

            f_handle.seek(-1, 1)
            f_handle.write(';\n')            
        
if __name__ == "__main__" :
    
    parser   = argparse.ArgumentParser()
    parser.add_argument("-s", "--sourcefile", default="sample.xml", help="Path to data file")
    parser.add_argument("-v", "--verbosity", default="DEBUG", help="set level of verbosity, DEBUG, INFO, WARN")
    parser.add_argument("-t", "--table",    required=True , help="database to dump data to")
    parser.add_argument("-l", "--logfile", default="./extract.log", help="Logfile path. Defaults to ./tabulator.log")

    args   = parser.parse_args()

    print "Processing : {0}".format(args.logfile)
    
    logging.basicConfig(filename=args.logfile, level=log_levels[args.verbosity],
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')

    logging.debug("Document processing starts")
    
    dataset = get_data(args.sourcefile, args.table, headers="implicit")
    #dump(dataset[0:10], keys, '', args.table, args.sourcefile.replace('.csv', '.sql'))

    #logging.debug("Document Complete:{0} with bad/total lines : {1}/{2}".format(args.sourcefile, bad, total))
    print "Done"

