# ISA Project 4 TA Guide

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
6. You should now be able to access our site at http://localhost:8000/

## Site Overview

Our site has two different types of accounts that you can sign up for: manufacturers and users. Since our website based on selling computer parts, computer hardware manufacturers can sign up for manufacturer accounts, which are able to create new listings. Users, on the other hand, cannot create new listings and can only browse available listings created by manufacturers.

## How To Use Our Site

When first visiting our website, you'll be greeted with the login screen. At the bottom of the screen you should see two buttons: one to sign up as a normal user, and one to sign up as a manufacturer. One thing to note is that when you are logging in as a manufacturer, your username will be the manufacturer name you entered in the sign up form.

When logged in as a mnufa


