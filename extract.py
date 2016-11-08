#!/usr/bin/env python
# coding: utf-8
import argparse
import mysql.connector
import logging
import xml.etree.cElementTree as ET
import sys

log_levels = { "DEBUG"   : logging.DEBUG,
               "INFO"    : logging.INFO,
               "WARNING" : logging.WARNING,
               "ERROR"   : logging.ERROR,
               "CRITICAL": logging.CRITICAL
}

def load_data(datafile):    
    context = ET.iterparse(datafile, events=("start", "end"))
    logging.debug("Got context")
    context = iter(context)    
    return context


def extract_editions(wos_id, elem):
    return [{'wos_id':wos_id,
             'edition': i.attrib['value']} for i in elem.iterfind('./static_data/summary/EWUID/edition')]


def extract_authors(wos_id, elem):
    authors = []
    
    for names in elem.iterfind('./static_data/summary/names'):
        for name in names:
            author = {'wos_id'   : wos_id,
                      'position' : name.attrib.get('seq_no', 'NULL'),
                      'reprint'  : name.attrib.get('reprint', 'NULL'),
                      'cluster_id': name.attrib.get('dais_id', 'NULL'),
                      'role'     : name.attrib.get('role','NULL')}
            for item in name.iter():
                author[str(item.tag)] = str(item.text)
            print author
            authors.extend(author)
        
        return authors
    
def extract_publisher(wos_id, elem):
    publisher = {'wos_id': wos_id}

    for publishers in elem.iterfind('./static_data/summary/publishers'):
        for item in publishers.iter():
            if item.tag in ['display_name', 'full_name', 'full_address', 'city']:
                publisher[item.tag] = item.text
    print publisher
    return publisher

def extract_addresses(wos_id, elem):
    addresslist = []
    print wos_id
    for addresses in elem.iterfind('./static_data/fullrecord_metadata/addresses/address_name'):
        
        print "-"*50
        
        addr = {'wos_id'   : wos_id,
                'addr_num' : list(addresses.iterfind('./address_spec'))[0].attrib['addr_no'],
                'organization' : 'NULL'
               }

        for address in addresses.iter():
            if address.tag in ['full_address', 'city', 'state', 'country', 'zip']:
                #print address.tag
                addr[str(address.tag)] =  str(address.text)

        orgs = []
        for item in addresses.iter():
            if item.tag == 'organization':
                orgs.extend([item.text])
        if not orgs :
            orgs = ['NULL']
        #print "Organizations : ", orgs
                    
        suborgs = []
        for item in addresses.iter():
            if item.tag == 'suborganization':
                suborgs.extend([item.text])
        if not suborgs :
            suborgs = ['NULL']

        #print "SubOrganizations : ", suborgs
        for org in orgs:
            for suborg in suborgs:
                t = {'organization'    : org,
                     'suborganization' : suborg}
                temp = addr.copy()
                temp.update(t)
                addresslist.extend([temp])
        #print addresslist
            
    #print addresslist
    return addresslist
        

def extract_authors(wos_id, elem):
    authors = []    
    
    for names in elem.iterfind('./static_data/summary/names'):
        for name in names:
            author = {'wos_id'   : wos_id,
                      'position' : name.attrib.get('seq_no', 'NULL'),
                      'reprint'  : name.attrib.get('reprint', 'NULL'),
                      'cluster_id': name.attrib.get('dais_id', 'NULL'),
                      'role'     : name.attrib.get('role','NULL')}
            for item in name.iter():
                author[str(item.tag)] = str(item.text)
            authors.extend(author)
        
    return authors

def extract_publisher(wos_id, elem):
    publisher = {'wos_id': wos_id}
    
    for publishers in elem.iterfind('./static_data/summary/publishers'):
        for item in publishers.iter():
            if item.tag in ['display_name', 'full_name', 'full_address', 'city']:
                publisher[item.tag] = item.text
                return publisher


def extract_pub_info(wos_id, elem):
    pub = {'wos_id': wos_id}

    try:
        # Add the page info
        pub.update(list(elem.iterfind('./static_data/summary/pub_info'))[0].attrib)
        #print elem.find('./static_data/summary/pub_info')
    except Exception as e:
        print "Caught error {0}".format(e)
        print list(elem.find('pub_info'))
        print pub
        logging.error("{0} Could not capture pub_info, Skipping document.".format(wos_id))
        raise 

    # Add the publication info    
    #pub.update(list(elem.iterfind('./static_data/summary/pub_info'))[0].attrib)
    
    # Get title, source, and source abbreviations   
    for i in elem.iterfind('./static_data/summary/titles/title'):
        pub[str(i.attrib['type'])] = i.text 
    
    # Get document type    
    try:
        pub['doc_type'] = list(elem.iterfind('./static_data/summary/doctypes/doctype'))[0].text
    except Exception as e:
        logging.warn("{0} Could not capture doctype, setting to default NULL".format(wos_id))
        pub['doc_type'] = 'NULL'

    # Add accession_no and issn
    for item in list(elem.iterfind('./dynamic_data/cluster_related/identifiers/identifier')):
        #print item.tag, item.attrib, item.text
        pub[item.attrib['type']] = item.attrib['value']

    # Oases gold    
    for item in list(elem.iterfind('./dynamic_data/ic_related/oases/oas')):
        print item.tag, item.attrib, item.text
        if item.text == 'Yes' and item.attrib['type'] == 'gold':
            pub['oases_type_gold'] = 'Yes'

    languages = []
    for lang in list(elem.iterfind('./static_data/fullrecord_metadata/languages/language')):
        #print lang.tag, lang.attrib, lang.text
        languages.extend([{'wos_id': wos_id,
                           'language' : lang.text}])
    # Get categorical data
    headings = []
    for x in list(elem.iterfind('./static_data/fullrecord_metadata/category_info/headings/heading')):
        headings.extend([{'wos_id': wos_id,
                          'heading': x.text }])
    
    subheadings = []
    for sub in list(elem.iterfind('./static_data/fullrecord_metadata/category_info/subheadings/subheading')):
        #print sub.tag, sub.attrib, sub.text
        subheadings.extend([{'wos_id': wos_id,
                             'subheading': sub.text }])
    #print "Subheadings : ", subheadings
    
    subjects = []
    for sub in list(elem.iterfind('./static_data/fullrecord_metadata/category_info/subjects/subject')):
        #print sub.tag, sub.attrib, sub.text
        subjects.extend([{'wos_id': wos_id,
                          'ascatype' : sub.attrib['ascatype'],
                          'subjects': sub.text }])
        
    return pub


if __name__ == "__main__" :
    
    parser   = argparse.ArgumentParser()
    parser.add_argument("-s", "--sourcefile", default="sample.xml", help="Path to data file")
    parser.add_argument("-v", "--verbosity", default="DEBUG", help="set level of verbosity, DEBUG, INFO, WARN")
    parser.add_argument("-l", "--logfile", default="./extract.log", help="Logfile path. Defaults to ./tabulator.log")

    args   = parser.parse_args()

    print "Processing : {0}".format(args.logfile)
    
    logging.basicConfig(filename=args.logfile, level=log_levels[args.verbosity],
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')

    logging.debug("Document processing starts")
    
    context = load_data(args.sourcefile)
    print "Done loading data into etree context"
    total = 0
    bad   = 0
    for event, elem in context:
        if event != "start" :
            continue
        pub = {} 
        if elem.tag == 'REC':
            total += 1
            try:
                wos_id = list(elem.iterfind('UID'))[0].text

                pub = extract_pub_info(wos_id, elem)            
                publisher = extract_publisher(wos_id, elem)
                authors = extract_authors(wos_id, elem)
                
            except Exception as e:
                print "Skipping... {0}".format(wos_id)
                bad += 1
        elem.clear()

    logging.debug("Document Complete:{0} with bad/total lines : {1}/{2}".format(args.sourcefile, bad, total))
    print "Done"

