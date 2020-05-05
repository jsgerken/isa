#!/bin/bash
docker pull mysql:latest
mkdir db
docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v ~/cs4501/db:/var/lib/mysql mysql:5.7
sleep 45
docker run -i -d --name mysql-cmdline --link mysql:db mysql:5.7 mysql -uroot -p'$3cureUS' -h db -e "create database cs4501 character set utf8;create user 'www'@'%' identified with mysql_native_password by '$3cureUS';grant all on *.* to 'www'@'%';flush privileges;"
sleep 20
