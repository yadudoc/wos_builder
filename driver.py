#!/usr/bin/env python
import argparse
import mysql.connector
import logging
import xml.etree.cElementTree as ET
import sys
import read_records as rr
import extract as x
from db_info import *
log_levels = { "DEBUG"   : logging.DEBUG,
               "INFO"    : logging.INFO,
               "WARNING" : logging.WARNING,
               "ERROR"   : logging.ERROR,
               "CRITICAL": logging.CRITICAL
}

def main (sourcefile):

    count  = 0
    logging.debug("Starting processing {0}".format(sourcefile))

    Pubs_list = []
    Lang_list = []
    Head_list = []
    Subh_list = []
    Subj_list = []
    Publ_list = []
    Auth_list = []
    Inst_list = []
    NaIn_list = []
    Edit_list = []
    Refs_list = []
    Ftxt_list = []
    Fund_list = []
    Keyw_list = []
    Keyp_list = []
    Conf_list = []
    CoSp_list = []
    
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
            
            Pub, Languages, Headings, Subheadings, Subjects    = x.extract_pub_info(wos_id, REC)
            Pubs_list.extend(Pub)
            Lang_list.extend(Languages)
            Head_list.extend(Headings)
            Subh_list.extend(Subheadings)
            Subj_list.extend(Subjects)
            
            #print pub
            Publishers = x.extract_publisher(wos_id, REC)
            Publ_list.extend(Publishers)
            
            
            #print publisher
            Authors   = x.extract_authors(wos_id, REC)
            Auth_list.extend(Authors)
            
            ##print authors
            Institutions, Name_inst_relation = x.extract_addresses(wos_id, REC)
            Inst_list.extend(Institutions)
            NaIn_list.extend(Name_inst_relation)
            #print len(Inst_list), Institutions
            #print len(NaIn_list), Name_inst_relation
            
            Editions = x.extract_editions(wos_id, REC)
            Edit_list.extend(Editions)

            References = x.extract_references(wos_id, REC)
            Refs_list.extend(References)

            #if references :
            #    print references[0]

            Ftext, Funding = x.extract_funding(wos_id, REC)
            Ftxt_list.extend(Ftext)
            Fund_list.extend(Funding)
            
            Conf, Sponsor  = x.extract_conferences(wos_id, REC)
            Conf_list.extend(Conf)
            CoSp_list.extend(Sponsor)
            #print len(Conf_list), Conf
            #print len(CoSp_list), Sponsor
            
            Keywords, Keywords_plus = x.extract_keywords(wos_id, REC)
            Keyw_list.extend(Keywords)
            Keyp_list.extend(Keywords_plus)
            #print Keywords

    print "Dumping results to .sql files"
    x.dump(Edit_list,    h_editions,       t_editions,         'editions',       'editions.sql')
    x.dump(Ftxt_list,    h_fundingtexts,   t_fundingtexts,     'fundingtext',    'fundingtext.sql')
    x.dump(Fund_list,    h_funding,        t_funding,          'funding',        'funding.sql')
    x.dump(Keyw_list,    h_keywords,       t_keywords,         'keywords',       'keywords.sql')
    x.dump(Keyp_list,    h_keywords_plus,  t_keywords_plus,    'keywords_plus',  'keywords_plus.sql')
    x.dump(Conf_list,    h_conferences,    t_conferences,      'conferences',    'conferences.sql')
    x.dump(CoSp_list,    h_conf_sponsors,  t_conf_sponsors,    'confSponsors',   'confSponsors.sql')
    x.dump(Refs_list,    h_references,     t_references,       'refs',           'references.sql')
    x.dump(Pubs_list,    h_publications,   t_publications,     'publications',   'publications.sql')
    x.dump(Lang_list,    h_languages,      t_languages,        'languages',      'langauges.sql')
    x.dump(Head_list,    h_headings,       t_headings,         'headings',       'headings.sql')
    x.dump(Subh_list,    h_subheadings,    t_subheadings,      'subheadings',    'subheadings.sql')
    x.dump(Subj_list,    h_subjects,       t_subjects,         'subjects',       'subjects.sql')
    x.dump(Publ_list,    h_publishers,     t_publishers,       'publishers',     'publishers.sql')
    x.dump(Auth_list,    h_contributors,   t_contributors,     'contributors',   'contributors.sql')
    x.dump(Inst_list,    h_institutions,   t_institutions,     'institutions',   'institutions.sql')
    x.dump(NaIn_list,    h_name_inst,      t_name_inst,        'affiliations',   'affiliations.sql')

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
    
