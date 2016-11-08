#!/usr/bin/env python

import argparse
import mysql.connector
#from elementtree.ElementTree import Element
#import cElementTree as ElementTree
import xml.etree.cElementTree as ET
import logging

log_levels = { "DEBUG"   : logging.DEBUG,
               "INFO"    : logging.INFO,
               "WARNING" : logging.WARNING,
               "ERROR"   : logging.ERROR,
               "CRITICAL": logging.CRITICAL
}


def tabulate(datafile, cnx):
   print "Tabulate"

   #tree = ET.parse(datafile)
   #root = tree.getroot()
   count = 0
   
   # get an iterable
   context = ET.iterparse(datafile, events=("start", "end"))
   logging.debug("Got context")
   # turn it into an iterator
   context = iter(context)

   # get the root element
   event, root = context.next()
   logging.debug("Got root")
   for event, elem in context:
      #if event == "start":
      #   print "Event:{0} \nElem:{1} \nAttr:{2} \nValue:{3}".format(event, elem.tag, elem.attrib, elem.value)
      
      if elem.tag == "REC" and event=="start":
         print "Foo"
         for child in elem:
            print child.tag, child.attrib
            
      #if event == "end" and elem.tag == "REC":
      #   print "Event:{0} Elem:{1}".format(event, elem)
      count = count+1
      root.clear()
      if count == 100:
         break
   '''
   for event, elem in tree.iterparse(datafile):
      print "Event:{0} Elem:{1}".format(event, elem)
      if elem.tag == "REC" :
         print "Foo"
      count = count + 1
      if count == 100:
         break
   '''

   return

   
if __name__ == "__main__":

   parser   = argparse.ArgumentParser()
   parser.add_argument("-s", "--sourcefile", required=True, help="Path to data file")
   parser.add_argument("-H", "--HOST",     default="wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com", help="Remote host db URL")
   parser.add_argument("-d", "--dbname",   required=True, help="DB to dump the data into")
   parser.add_argument("-u", "--username",   required=True, help="Username")
   parser.add_argument("-p", "--password",   required=True, help="Password")  
   parser.add_argument("-v", "--verbosity", default="DEBUG", help="set level of verbosity, DEBUG, INFO, WARN")
   parser.add_argument("-l", "--logfile", default="tabulator.log", help="Logfile path. Defaults to ./tabulator.log")

   args   = parser.parse_args()

   logging.basicConfig(filename=args.logfile, level=log_levels[args.verbosity],
                       format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                       datefmt='%m-%d %H:%M')

   cnx = mysql.connector.connect(user=args.username, password=args.password,
                                 host=args.HOST,
                                 database=args.dbname)
   
   tabulate(args.sourcefile, cnx)
   cnx.close()
   
