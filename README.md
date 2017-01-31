[![Build Status](https://travis-ci.org/andela-gochieng/Bucketlist-flask-api.svg?branch=develop)](https://travis-ci.org/andela-gochieng/Bucketlist-flask-api)
[![Code Climate](https://codeclimate.com/github/andela-gochieng/Bucketlist-flask-api/badges/gpa.svg)](https://codeclimate.com/github/andela-gochieng/Bucketlist-flask-api)
[![Code Health](https://landscape.io/github/andela-gochieng/Bucketlist-flask-api/develop/landscape.svg?style=flat)](https://landscape.io/github/andela-gochieng/Bucketlist-flask-api/develop)
[![Test Coverage](https://codeclimate.com/github/andela-gochieng/Bucketlist-flask-api/badges/coverage.svg)](https://codeclimate.com/github/andela-gochieng/Bucketlist-flask-api/coverage)
## Bucketlist Flask API
This is a RESTful API for an online Bucket List service using Flask.
It allows for the:
* Creation and viewing of various bucketlists
* Addition of items to a bucketlist of choice
* Editing of the bucketlists and items
* Deleting of the bucketlists and/or items

### Getting started
Clone this repo from Github to your local machine:
```
git clone git@github.com:andela-gochieng/Bucketlist-flask-api.git
```
cd into the Bucketlist folder
```
cd Bucketlist
```
Create a virtual environment

Install the dependencies
```
pip install -r requirements.txt
```
Run the program
```
python run.py 
```
##API Endpoints
| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/api/v1/auth/register` | POST  | Register user | FALSE |
|  `/api/v1/auth/login` | POST | Login user | FALSE |
| `/api/v1/bucketlists/` | GET, POST | View user's bucketlists | TRUE |
| `/api/v1/bucketlists/<id>` | GET, PUT, DELETE | Change single bucketlist | TRUE |
| `/api/v1/bucketlists/<id>/items/` | GET, POST | View items in a bucketlist | TRUE |
| `/api/v1/bucketlists/<id>/items/<item_id>` | GET, PUT, DELETE| A single bucketlist item | TRUE |
