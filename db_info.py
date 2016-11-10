#!/usr/bin/env python


h_publishers      = ['wos_id', # Primary key
                   'display_name', 'full_name', 'full_address', 'city']
t_publishers      = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40) PRIMARY KEY,
    display_name varchar(200),
    full_name    varchar(200),
    full_address varchar(200),
    city         varchar(50)
);
"""


print "*"*50
print "WARNING , Publication abstract is disabled"
print "*"*50

h_publications    = ['wos_id', # Primary key 
                     'accession_no', 'issn', 'eissn', 'doi', # cluster_related
                     'doc_type', 'title', 'pubyear', 'pubmonth', 'coverdate', 'sortdate',
                     'vol', 'pubtype','issue',
                     'supplement', 'special_issue', 'part_no',
                     'indicator', 'is_archive', 'city', 'country',
                     'oases_type_gold', 'has_abstract' ]
                     #'abstract']
t_publications    = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id          varchar(40) PRIMARY KEY,

    accession_no    varchar(10),
    issn            varchar(20),
    eissn           varchar(20),
    doi             varchar(50),
    
    doc_type        varchar(20),
    title           varchar(100),
    pubyear         varchar(4),
    pubmonth        varchar(10),
    coverdate       varchar(15), 
    sortdate        varchar(15),

    vol             varchar(5),
    pubtype         varchar(15),
    issue           varchar(5),
    supplement      varchar(5),
    special_issue   varchar(5),
    part_no         varchar(5),
    indicator       varchar(5),
    is_archive      varchar(5),
    city            varchar(20),
    country         varchar(20),
    has_abstract    varchar(5),
    oases_type_gold varchar(5),
    abstract        varchar(3000) DEFAULT NULL
);
"""


h_editions        = ['wos_id', 'edition']
t_editions        = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    edition varchar(20)
);
"""

h_contributors    = ['wos_id', 'position', #Primary key
                   'reprint', 'cluster_id', 'role', 'orcid_id', 'orcid_id_tr',
                   'display_name', 'full_name', 'wos_standard',
                   'first_name', 'last_name', 'email_addr']
t_contributors    = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id       varchar(40),
    position     varchar(5),
    reprint      varchar(5),
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
);
"""


h_institutions    = ['wos_id', 'addr_num', # Duplication in org and suborg prevents primary key
                   'organization', 'suborganization',
                   'full_address', 'city', 'state', 'country', 'zip' ]
t_institutions    = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id           varchar(40),
    addr_num         varchar(5),
    organization     varchar(200),
    suborganization  varchar(200),
    full_address     varchar(200),
    city             varchar(50),
    state            varchar(50),
    country          varchar(50),
    zip              varchar(20)
);
"""

h_name_inst       = ['wos_id', 'position', 'addr_num']
t_name_inst       = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id           varchar(40),
    position         varchar(5),
    addr_num         varchar(5)
);
"""

h_references      = ['wos_id', 'uid', # Primary key
                     'citedAuthor', 'year', 'page', 'volume', 'citedTitle',
                     'citedWork', 'doi', 'art_no', 'patent_no']
t_references      = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    uid varchar(50),
    citedAuthor varchar(100),
    year   varchar(10),
    page   varchar(5),
    volume varchar(5),
    citedTitle varchar(500),
    citedWork  varchar(100),
    doi        varchar(50),
    art_no     varchar(20),
    patent_no  varchar(20)
);
"""

h_fundingtexts    = ['wos_id', # Primary key
                     'funding_text']
t_fundingtexts    = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    funding_text varchar(1000)
);
"""


h_funding         = ['wos_id', 'agency', 'grant_id']
t_funding         = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    agency varchar(200),
    grant_id varchar(50)
);
"""

h_keywords        = ['wos_id', 'keyword']
t_keywords        = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(100)
);
"""

h_keywords_plus   = ['wos_id', 'keyword']
t_keywords_plus   = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    keyword varchar(100)
);
"""

h_languages       = ['wos_id', 'language']
t_languages       = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    language varchar(50)
);
"""

h_subheadings       = ['wos_id', 'subheading']
t_subheadings       = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    subheading varchar(100)
);
"""

h_headings       = ['wos_id', 'heading']
t_headings       = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    heading varchar(100)
);
"""

h_subjects       = ['wos_id', 'subject', 'ascatype']
t_subjects       = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id varchar(40),
    ascatype varchar(40),
    subject varchar(100)
);
"""

h_conferences    = ['wos_id', 'conf_id', # Primary key
                    'info', 'title', 'dates', 'conf_city', 'conf_state', 'conf_host']
t_conferences    = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id    varchar(40),
    conf_id   varchar(15),
    info      varchar(500),
    title     varchar(200),
    dates     varchar(50),
    conf_city varchar(50),
    conf_state varchar(50),
    conf_host  varchar(100),
    PRIMARY KEY (wos_id, conf_id)
);
"""

h_conf_sponsors  = ['wos_id', 'conf_id', 'sponsor']
t_conf_sponsors  = """
USE wos;
-- DROP TABLE IF EXISTS {0}; 
CREATE TABLE {0} ( 
    wos_id  varchar(40),
    conf_id varchar(15),
    sponsor varchar(100)
);
"""




