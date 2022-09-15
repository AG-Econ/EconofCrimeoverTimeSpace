# Overview

This lecture+masterclass aims to give a knowhow of 1) scrape data from dynamic websites, 2) work with unstructured data. This is the readme file which gives all files/slides/codes for the talk. 

# Instructions
I'll be working with Python 3.10. If you haven't used Python before, I recommend PyCharm IDE (integrated development environment). It's available here (community version): https://www.jetbrains.com/pycharm/download/

We will also need to have Firefox driver installed for the webscraping part. You might prefer to use other drivers like Google (in that case you will need to rectify the web.browser command in the main.py).

# Installing packages

There are a few packages we'll go through that you need to install. Some basic general-use Python libraries you'll need to install:
re 
csv
time
pandas
numpy
matplotlib
statsmodels

Then some more scraping; natural language processing or machine learning; mapping specific packages:
selenium
spacy
geopy
geocoders
folium
sklearn
nltk

If you're using PyCharm, in the bottom-right corner of the screen it will say something like "Python 3.10" to tell you which Python interpreter PyCharm is using. If you click on this, then on "Interpreter Settings" in the menu that pops up, it will list the packages installed. At the bottom of this list there will be a "+" symbol that allows you to install new packages. If you click the "+" button, it will bring up a list of available packages, and you can search by name for the packages listed above, and it will automatically install for you.

# Datafile descriptions

Datafile 1: london_places.csv - this is a data I am providing from Wikipedia (https://en.wikipedia.org/wiki/List_of_areas_of_London). I have done 3 modifications to it for the sake of simplicity but this should be adjusted to research objectives and equally (preferably) doable in Python. 
          a) If there are more than one postcode district for a location, I have kept the 1st one listed (one can work out the largest area etc to use the corresponding postcode district etc).
          b) If there were more than 1 location listed in each cell of locations, I added these as seperate observations in the file, with the same postcode district. 
          c) I have renamed the variable Postcode district to Postcodedistrict for convenience.
The only 2 columns of interest here for us are Location and Postcodedistrict.          


Datafile 2: Scraped data from the ...


Datefile 3: URLs


Set of slides 1: Webscraping

Set of slides 2: Text as Data

Code 1: urls extractor

Code 2: scraper

Code 3: prelim_textasdata

Code 4: final_textasdata

# Declarations

I do cheat a little in this class. Pre-processing of datafile 1 should be done in Python. Some codes can be more efficient (writing loops/functions). 

# Sources
