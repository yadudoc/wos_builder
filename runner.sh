#!/bin/bash

installs() {
    apt-get update
    apt-get -y install unzip gzip mysql-client-5.6
}

setup_data() {
    pushd .
    cd ..
    zipfile=`ls *zip`
    echo "Found zip file : ", $zipfile
    unzip $zipfile;
    for gz in `echo *gz`
    do
	echo "Gunzipping $gz"
	gunzip $gz;
    done
    popd
}

extract_data() {
    pushd .
    chmod a+x driver.py
    for xml in `echo ../*xml`
    do
	./driver.py -s $xml -l ../extract.log -d ../sqldata

	for sql in $(echo ../sqldata/*sql)
	do
	    echo "Loading file $sql extracted from $xml to wos2"
	    mysql -h wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com \
		  -P 3306 \
		  -u $wosuser \
		  -p$wospasswd < $sql
	done
	echo "Exiting early"
	return
	
    done
    popd
}

get_year() {
    year=''
    echo ../*zip &> /dev/null
    if [[ $? -eq 0 ]]
    then
	year=$(basename ../*zip | cut -c -5)
	echo $year
    else
	echo ''	
    fi
}

flush_db() {
cat <<EOF > flush.sql
use wos;
DROP TABLE IF EXISTS $1affiliations ;
DROP TABLE IF EXISTS $1confSponsors ;
DROP TABLE IF EXISTS $1conferences  ;
DROP TABLE IF EXISTS $1contributors ;
DROP TABLE IF EXISTS $1editions     ;
DROP TABLE IF EXISTS $1funding      ;
DROP TABLE IF EXISTS $1fundingtext  ;
DROP TABLE IF EXISTS $1headings     ;
DROP TABLE IF EXISTS $1institutions ;
DROP TABLE IF EXISTS $1keywords     ;
DROP TABLE IF EXISTS $1keywords_plus;
DROP TABLE IF EXISTS $1languages    ;
DROP TABLE IF EXISTS $1publications ;
DROP TABLE IF EXISTS $1publishers   ;
DROP TABLE IF EXISTS $1refs         ;
DROP TABLE IF EXISTS $1subheadings  ;
DROP TABLE IF EXISTS $1subjects     ;
EOF
    echo "Dropping all tables with $1 prefix"
    mysql -h wos2.cvirc91pe37a.us-east-1.rds.amazonaws.com \
	  -P 3306 \
	  -u $wosuser \
	  -p$wospasswd < flush.sql
}


# Install packages
installs
# Setup the data files
setup_data

# Flush the DB for this year's tables
year=$(get_year)
flush_db $year

# Extract and dump data to DB
extract_data
