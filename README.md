# Cupboard-Companion
Welcome to Cupboard Companion!

Cupboard Companion is a service designed to help college students (and other kinds of people who just don't have tons of time and money to devote to cooking) find quick, simple recipes that use up ingredients they already have on hand. We get a list of ingredients from a user and, using the Yummly API, gather recipes that contain those items. Then we process the results based on the number of ingredients, the complexity of the instructions, and some other important factors to determine what recipes are the easiest to prepare. 

## How to Run
### Web App
The web application for this project is run via Flask. Once installed, simply go into the app directory and type ```python app.py```.

This will open up the application on localhost. Open any web browser and go to 127.0.0.1:5000 to begin using the cupboard companion tool
### Core Algorithm
The core algorithm itself is run via python, version 2.7+

User input is currently taken via a text file. Each ingredient should be on its own line in that file, and ingredients can be multiple words (e.g. bell pepper). To run the program, simply input the command ```python data_collection.py [input file name].txt```

This will return the top 20 recipes for the given ingredients, each with a "simplicty score" that determines the ranking. 

It is necessary to install all dependencies described below before attempting to run this script.

## Dependencies
The web application is built off of Flask. In order to run the web application, it is necesary that Flask is installed. Instructions can be found on the following page:
http://flask.pocoo.org/

We use the BeautifulSoup library to pull recipe instructions out of HTML files. To run our program, it is necessary that you have BeautifulSoup installed. Instructions can be found on the following page: 
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

Another package we use is textstat 0.2. This package has functions that help us determine the complexity of the recipe directions. Instructions can be found on the following page:
https://pypi.python.org/pypi/textstat/0.2

## Usage
```python data_collection.py query.txt```

## Common Cupboard

```common_cupboard.py``` was used to collect information from a bunch of random recipes on the Yummly API, and build a sort of "common cupboard", which would contain ingredients that most people would have on hand. We assume, in the algorithm, that people would have enough of each of these ingredients to make any of the returned recipes.


