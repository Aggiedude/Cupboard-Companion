# Cupboard-Companion
Welcome to Cupboard Companion!

Cupboard Companion is a service designed to help college students (and other kinds of people who just don't have tons of time and money to devote to cooking) find quick, simple recipes that use up ingredients they already have on hand. We get a list of ingredients from a user and, using the Yummly API, gather recipes that contain those items. Then we process the results based on the number of ingredients, the complexity of the instructions, and some other important factors to determine what recipes are the easiest to prepare. 

We use the BeautifulSoup library to pull recipe instructions out of HTML files. To run our program, it is necessary that you have BeautifulSoup installed. Instructions can be found on the following page: 
https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

Another package we use is textstat 0.2. This package has functions that help us determine the complexity of the recipe directions. Instructions can be found on the following page:
https://pypi.python.org/pypi/textstat/0.2

Usage: python data_collection.py query.txt
