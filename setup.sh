#!/bin/bash
docker pull mysql:latest
mkdir -p ~/cs4501/db
docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v ~/cs4501/db:/var/lib/mysql mysql:latest
sleep 20
docker exec mysql mysql -uroot -p'$3cureUS' -se "create user 'www'@'%' identified with mysql_native_password by '$3cureUS';create database cs4501 character set utf8;grant all on *.* to 'www'@'%';" &> /dev/null
sleep 5
docker exec mysql mysql -uroot -p'$3cureUS' -se "create user 'www'@'%' identified with mysql_native_password by '$3cureUS';create database cs4501 character set utf8;grant all on *.* to 'www'@'%';" &> /dev/null
sleep 5
docker exec mysql mysql -uroot -p'$3cureUS' -se "create user 'www'@'%' identified with mysql_native_password by '$3cureUS';create database cs4501 character set utf8;grant all on *.* to 'www'@'%';" &> /dev/null
sleep 5
docker exec mysql mysql -uroot -p'$3cureUS' -se "create user 'www'@'%' identified with mysql_native_password by '$3cureUS';create database cs4501 character set utf8;grant all on *.* to 'www'@'%';" &> /dev/null
sleep 5
docker exec mysql mysql -uroot -p'$3cureUS' -se "create user 'www'@'%' identified with mysql_native_password by '$3cureUS';create database cs4501 character set utf8;grant all on *.* to 'www'@'%';" &> /dev/null
sleep 20
