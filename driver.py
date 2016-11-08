#!/usr/bin/env python
import argparse
import mysql.connector
import logging
import xml.etree.cElementTree as ET
import sys
import read_records as rr
import extract as x

log_levels = { "DEBUG"   : logging.DEBUG,
               "INFO"    : logging.INFO,
               "WARNING" : logging.WARNING,
               "ERROR"   : logging.ERROR,
               "CRITICAL": logging.CRITICAL
}


def main (sourcefile):

    count  = 0
    logging.debug("Starting processing {0}".format(sourcefile))
    with open(args.sourcefile, 'r') as data:

        while True:
            count  += 1
            record  = rr.get_record(data)
            
            if not record:
                logging.debug("Completed processing {0}".format(sourcefile))
                print "Processed {0} records".format(count-1)
                break

            #context = extract.load_data(record)
            REC    = ET.fromstring(record)
            wos_id = list(REC.iterfind('UID'))[0].text
            
            pub       = x.extract_pub_info(wos_id, REC)
            #print pub
            publisher = x.extract_publisher(wos_id, REC)
            #print publisher
            authors   = x.extract_authors(wos_id, REC)
            #print authors
            institutions = x.extract_addresses(wos_id, REC)
    return

    
if __name__ == "__main__" :
    
    parser   = argparse.ArgumentParser()
    parser.add_argument("-s", "--sourcefile", default="sample.xml", help="Path to data file")
    parser.add_argument("-v", "--verbosity", default="DEBUG", help="set level of verbosity, DEBUG, INFO, WARN")
    parser.add_argument("-l", "--logfile", default="./extract.log", help="Logfile path. Defaults to ./tabulator.log")

    args   = parser.parse_args()

    print "Processing : {0}".format(args.sourcefile)
    
    logging.basicConfig(filename=args.logfile, level=log_levels[args.verbosity],
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')

    logging.debug("Document processing starts")
    main(args.sourcefile)
    
