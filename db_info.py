#!/usr/bin/env python


h_publishers      = ['wos_id', # Primary key
                   'display_name', 'full_name', 'full_address', 'city']
t_publishers      = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40) PRIMARY KEY,
    display_name varchar(100),
    full_name    varchar(100),
    full_address varchar(100),
    city         varchar(50)
)
"""


h_publications    = ['wos_id', # Primary key 
                     'accession_no', 'issn', 'eissn', 'doi', # cluster_related
                     'doc_type', 'title', 'pubyear', 'pubmonth', 'coverdate', 'sortdate',
                     'vol', 'pubtype','issue',
                     'supplement', 'special_issue', 'part_no',
                     'indicator', 'is_archive', 'city', 'country',
                     'oases_type_gold', 'has_abstract',
                     'abstract']
t_publications    = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40) PRIMARY KEY,

    accession_no varchar(10),
    issn         varchar(20),
    eissn        varchar(20),
    doi          varchar(20),
    
    doctype      varchar(20),
    title        varchar(100),
    pubyear      varchar(4),
    pubmonth     varchar(10),
    coverdate    varchar(15), 
    sortdate     varchar(15),

    vol          varchar(5),
    pubtype      varchar(15),
    issue        varchar(5),
    supplement   varchar(5),
    special_issue varchar(5),
    part_no      varchar(5),
    indicator    varchar(5),
    is_archive   varchar(2),
    city         varchar(20),
    country      varchar(20),
    has_abstract varchar(2),
    abstract     varchar(3000)
)
"""


h_editions        = ['wos_id', 'edition']
t_editions        = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    edition varchar(20)
)
"""

h_contributors    = ['wos_id', 'position', #Primary key
                   'reprint', 'cluster_id', 'role', 'orcid_id', 'orcid_id_tr',
                   'display_name', 'full_name', 'wos_standard',
                   'first_name', 'last_name', 'email_addr']
t_contributors    = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id       varchar(40),
    position     varchar(2),
    reprint      varchar(2),
    cluster_id   varchar(10),
    role         varchar(10),
    orcid_id     varchar(15),
    orcid_id_tr  varchar(15),
    display_name varchar(50),
    full_name    varchar(50),
    wos_standard varchar(50),
    first_name   varchar(50),
    last_name    varchar(50),
    email_addr   varchar(50),
    PRIMARY KEY (wos_id, position)
)
"""


h_institutions    = ['wos_id', 'addr_num', # Duplication in org and suborg prevents primary key
                   'organization', 'suborganization',
                   'full_address', 'city', 'state', 'country', 'zip' ]
t_institutions    = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(50)
)
"""

h_name_inst       = ['wos_id', 'position', 'addr_num']
t_name_inst       = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(50)
)
"""

h_references      = ['wos_id', 'uid', # Primary key
                   'citedAuthor', 'year', 'page', 'volume', 'citedTitle',
                   'citedWork', 'doi', 'art_no', 'patent_no']
t_references      = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(50)
)
"""

h_fundingtexts    = ['wos_id', # Primary key
                   'funding_text']
t_fundingtexts    = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(50)
)
"""


h_funding         = ['wos_id', 'agency', 'grant_id']
t_funding         = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(50)
)
"""


h_conference      = ['wos_id', 'conf_id', # Primary key
                     'info', 'title', 'dates', 'conf_city', 'conf_state', 'conf_host']
t_conference      = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(50)
)
"""


h_sponsors        = ['wos_id', 'conf_id', 'sponsor']
t_sponsors        = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    conf_id int,
    sponsor varchar(100)
)
"""

h_keywords        = ['wos_id', 'keyword']
t_keywords        = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(50)
)
"""

h_keywords_plus   = ['wos_id', 'keyword']
t_keywords_plus   = """
DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(50)
)
"""


