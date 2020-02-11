# ISA Project 2: API Guide

## Setup
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
- Docker compose up will open port at `http://localhost:8001/`
### Manufacturers
- **Get All Users**
  * **Description:**
    * Returns json data that list all Manufacturers
  * **URL:**
    * api/v1/manufacturers/
  * **Method:**
    * `GET`
  * **Sample Curl:** 
    * `curl http://localhost:8001/api/v1/manufacturers/`
- **Get manufacturer by id**
  * **Description:**
    * Returns json data for Manufacturer with specified id
  * **URL:**
    * api/v1/manufacturers/<man_id>
  * **Method:**
    * `GET`
  * **Sample Curl:** 
    * `curl http://localhost:8001/api/v1/manufacturers/1`
- **Update Manufacturer by id**
  * **Description:**
    * Returns json data for Manufacturer with specified id ???
  * **URL:**
    * api/v1/manufacturers/<man_id>
  * **Method:**
    * `POST`
  * **Sample Curl:** 
    * `curl -d "man_name=Gigabyte&web_url=gigabyte.net&phone_num=54321" -H "Content-Type: application/x-www-form-urlencoded" -X POST`
### Products

