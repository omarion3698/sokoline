# sokoline

## Authors
  * Omar Hussein
  * Aoko Mercyline
  * George Kilewa
  * Langat K Justus
  
## Description
A website where a user can be a seller/buyer by posting items in the Market currently and pay the money online using either PayPal or Mastercard.

## User Stories

* Authenticate users via email token.
* It should have an Admin/Client dashboard.
* A user can register as a seller/buyer.
* A seller can post items in the Market.
* A user can see the preview of the items without necessarily signing up/logging in.
* A user can comment on the items by making a review on it.
* A user can add items to cart.
* A user can specify the delivery address.
* A user can make payment using electronic methods.
* A user can view the delivery process.
* A user can have an invoice describing the items he/she has bought.

## Setup Instructions

To come up with the same project...

##### Clone the repository:
  * https://github.com/omarion3698/sokoline.git
  
##### Navigate into the folder and install requirements
  * cd sokoline 
  * pip install -r requirements.txt
  
##### Install and activate Virtual environment
  * virtualenv venv
  * source venv/bin/activate
  
##### Install Dependencies
  * pip install -r requirements.txt
  
##### Setup Database
##### SetUp your database User,Password, Host then make migrate
  * python manage.py makemigrations users
  
##### Now Migrate
  * python manage.py migrate
  
##### Run the application
  * python manage.py runserver
  
##### Testing the application
  * python manage.py test
  
Open the application on your browser 127.0.0.1:8000.

## Technologies Used
* Python3.8
* Django
* Heroku

## Contact Information
If you have any questions or contributions, please email us at:
* omaribinbakarivic@gmail.com
* aokomercyline34@gmail.com
* kilewageorge230@gmail.com
* justuslangat78@gmail.com

## License
* Licensed under the [MIT License](LICENSE)
* Copyright (c) 2020 Omar Hussein.
