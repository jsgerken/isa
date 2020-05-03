#!/bin/bash
mysql -uroot -p'$3cureUS' -h db
create user 'www'@'%' identified with mysql_native_password by '$3cureUS';
create database cs4501 character set utf8;
grant all on cs4501.* to 'www'@'%';
quit
