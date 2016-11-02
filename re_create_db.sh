#!/bin/bash

if [[ $# != 4 ]]
then
    echo "Usage $0 <db_host> <db_username> <db_password> <db_name>"
    exit -1
fi

db_host=$1
db_username=$2
db_password=$3
db_name=$4

cat <<EOF > 'create.sql'
drop database if exists $db_name;
create database $db_name;
use $db_name;

create table

EOF

mysql -h $db_host -P 3306 -u $db_username -p$db_password < create.sql
