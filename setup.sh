#!/bin/bash
docker pull mysql:latest
mkdir db
docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v ~/cs4501/db:/var/lib/mysql mysql:latest
sleep 45
docker exec -i mysql mysql -uroot -p'$3cureUS' -e "create user 'www'@'%' identified with mysql_native_password by '$3cureUS';"
docker exec -i mysql mysql -uroot -p'$3cureUS' -e "create database cs4501 character set utf8;"
docker exec -i mysql mysql -uroot -p'$3cureUS' -e "grant all on *.* to 'www'@'%';"
sleep 20
