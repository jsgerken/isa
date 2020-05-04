#!/bin/bash
docker pull mysql:latest
mkdir -p ~/cs4501/db
docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v ~/cs4501/db:/var/lib/mysql mysql:latest
sleep 20
docker exec -i mysql /bin/bash/ -c 'mysql -uroot -p'$3cureUS' << EOF'
create user 'www'@'%' identified with mysql_native_password by '$3cureUS';
create database cs4501 character set utf8;
grant all on *.* to 'www'@'%';
quit
EOF
sleep 20
docker-compose up -d
docker network connect isa_backend mysql
docker ps
