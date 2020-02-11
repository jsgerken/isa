# ISA Project 2: API Guide

## Installation 
1. Clone this repository
2. Run the following comand to start the container and initialize the network
```shell
docker-compose up
```  
3. It will error initially, exit out of the container
4. Run the following command to connect the mysql container to the created network
```shell
docker network connect isa_backend mysql
``` 
5. Rerun the following command
```shell
docker-compose up
```  
6. Congratulations, you're now ready to access our project API

## API Endpoints


