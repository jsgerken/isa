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
- **Get all Manufacturers**
  * **Description:**
    * Returns json array containing all Manufacturers
  * **URL:**
    * api/v1/manufacturers/
  * **Method:**
    * `GET`
  * **Sample Curl:** 
    * `curl http://localhost:8001/api/v1/manufacturers/`
- **Get Manufacturer by id**
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
    * Updates passed in data for Manufacturer with specified id 
  * **URL:**
    * api/v1/manufacturers/<man_id>
  * **Method:**
    * `POST`
  * **Expected Body Parameters:**
    * man_name: String
    * web_url: String
    * phone_num: Integer
  * **Sample Curl:** 
    * `curl -d "man_name=Gigabyte&web_url=gigabyte.net&phone_num=54321" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8001/api/v1/manufacturers/3`
- **Delete a Manufacturer by id**
  * **Description:**
    * Deletes Manufacturer with specified id, returning the deleted object as json
  * **URL:**
    * api/v1/manufacturers/<man_id>/delete/
  * **Method:**
    * `DELETE`
  * **Sample Curl:** 
    * `curl -X DELETE http://localhost:8001/api/v1/manufacturers/1/delete/`
- **Create a Manufacturer**
  * **Description:**
    * Creates new Manufacturer with given params, returns newly created object as json
  * **URL:**
    * api/v1/manufacturers/create/ (DOUBLE CHECK ME)
  * **Method:**
    * `POST`
  * **Expected Body Parameters:**
    * man_name: String
    * web_url: String
    * phone_num: Integer
  * **Sample Curl:** 
    * `curl -d "man_name=Gigabyte&web_url=gigabyte.net&phone_num=54321" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8001/api/v1/manufacturers/create/`
### Products
- **Get all Products**
  * **Description:**
    * Returns json array containing all Products
  * **URL:**
    * api/v1/products/
  * **Method:**
    * `GET`
  * **Sample Curl:** 
    * `curl http://localhost:8001/api/v1/products/`
- **Get Product by id**
  * **Description:**
    * Returns json data for Product with specified id
  * **URL:**
    * api/v1/products/<product_id>
  * **Method:**
    * `GET`
  * **Sample Curl:** 
    * `curl http://localhost:8001/api/v1/products/1`
- **Update Product by id**
  * **Description:**
    * Updates passed in data for Product with specified id 
  * **URL:**
    * api/v1/products/<product_id>
  * **Method:**
    * `POST`
  * **Expected Body Parameters:**
    * name: String
    * type: String
    * price: Integer
    * description: String
    * warranty: String
    * man_id: Integer
  * **Sample Curl:** 
    * `curl -d "name=TestNameUpd&type=TestTypeUpdt&price=123&description=TestDescUpd&warranty=TestWarrantyUpd&man_id=3" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8001/api/v1/products/3/create/`
- **Delete a Product by id**
  * **Description:**
    * Deletes Manufacturer with specified id, returning the deleted object as json
  * **URL:**
    * api/v1/manufacturers/<product_id>/delete/
  * **Method:**
    * `DELETE`
  * **Sample Curl:** 
    * `curl -X DELETE http://localhost:8001/api/v1/manufacturers/1/delete/`
- **Create a Product**
  * **Description:**
    * Creates new Manufacturer with given params, returns newly created object as json
  * **URL:**
    * api/v1/manufacturers/create/ (DOUBLE CHECK ME)
  * **Method:**
    * `POST`
  * **Expected Body Parameters:**
    * name: String
    * type: String
    * price: Integer
    * description: String
    * warranty: String
    * man_id: Integer
  * **Sample Curl:** 
    * `curl -d "name=TestNameCreate&type=TestTypeCreatet&price=123&description=TestDescCreate&warranty=TestWarrantyCreate&man_id=3" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8001/api/v1/products/create/`

