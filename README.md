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

Our site has two different types of accounts that you can sign up for: manufacturers and users. Since our website is based on selling computer parts, computer hardware manufacturers can sign up for manufacturer accounts, which are able to create new listings. Users, on the other hand, cannot create new listings and can only browse available listings created by manufacturers.

## How To Use Our Site

When first visiting our website, you'll be greeted with the login screen. At the bottom of the screen you should see two buttons: one to sign up as a normal user, and one to sign up as a manufacturer. One thing to note is that when you are logging in as a manufacturer, your username will be the manufacturer name you entered in the sign up form, and you will need to check the "I am a manufacturer" box above the login button. 

When logged in as a manufacturer, you are able to access the create listing button on the right side of the navbar. It will take you to a form to fill out some information about the product, and after filling out the form you will be brought to the product details page for the listing you just created. You will also be able to see the product added to the newest product carousel on the home page (although you may have to click the arrows to have it be displayed).

Extra Credit: User Profile

When logged in as a user, you are able to access the user profile page button on the right side of the navbar. It will take you to a screen displaying some of the information entered when signing up as a user. If you would like to update this information, you canc lick the Edit button at the bottom of the page to be brought to a form to fill out new information. It should then bring you back to the profile page and display any changes you have made.

Extra Credit: Password Reset

If you navigate to the login screen either by typing in the URL or clicking the sign out button when logged in, you can click the "Forgot Your Password?" button located just underneath the login button to reset your password. On the page you are brought to, you can either enter your username, manufacturer name, or email, along with checking the manufacturer box if necesarry, to be emailed a password reset link. Note that this link is emailed to the email associated with a user/manufacturer in the database, so to properly test it make sure you have an account with an email you can access.




