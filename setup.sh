#!/bin/bash
docker pull mysql:5.7
mkdir db
docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v ~/cs4501/db:/var/lib/mysql mysql:5.7
sleep 45
