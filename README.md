# Summer School: The Economics Crime over Time and Space: Theory, Practice and Applications

## Overview

These sessions aim to give a knowhow of 1) scraping data from dynamic websites (session 1), 2) working with unstructured text (session 2). We will use the following website to get our data and work with it: https://www.murdermap.co.uk/. There is a lot of ground to cover, so I will be at places skipping some basic steps. It might be difficult to follow with running all the codes, unless you are already quite comfortable with Python. This is the readme file which gives all files/slides/codes for the talk. 

## Instructions

I'll be working with Python 3.10. If you haven't used Python before, I recommend PyCharm IDE (integrated development environment). It's available here (community version): https://www.jetbrains.com/pycharm/download/

We will use Google Chrome to inspect the HTMLs for scraping but will use Firefox driver installed for the actual webscraping part. You might prefer to use other drivers like Google (in that case you will need to rectify the web.browser command in the main.py).

For ethical reasons (and practical reason of not overloading the target website with 30+ requests)- I suggest that you follow the lecture and see me use the code for scraping to get the data in the first part. If you are interested in practicing you can do so later and I will be happy to answer further questions over email for this part.

For the second part, I have already provided the datafile I obtained with this scraping code and you can follow along the code with me, if you wish. 

## Installing packages

There are a few packages we'll use that you need to install. Some basic general-use Python libraries you'll need to install (or probably already have):
* re 
* os
* csv
* time
* pandas
* numpy
* matplotlib
* statsmodels

Then some more scraping; natural language processing or machine learning; mapping specific packages:
* selenium
* spacy
* geopy
* geocoders
* folium
* sklearn
* nltk

If you're using PyCharm, in the bottom-right corner of the screen it will say something like "Python 3.10" to tell you which Python interpreter PyCharm is using. If you click on this, then on "Interpreter Settings" in the menu that pops up, it will list the packages installed. At the bottom of this list there will be a "+" symbol that allows you to install new packages. If you click the "+" button, it will bring up a list of available packages, and you can search by name for the packages listed above, and it will automatically install for you.

## File descriptions

**Datafile 1:** url_collector.csv - this file contains the specific urls from which we scrape the intended data (output from main.py, and used as input in Scraper.py: session 1)

**Datefile 2:** raw_data.csv - this file contains the scraped data obtained from the Scraper.py code below (output from session 1). This is also the input file for us to work in session 2. 

**Datafile 3:** london_places.csv - this is a data I am providing from Wikipedia (https://en.wikipedia.org/wiki/List_of_areas_of_London). I have done 3 modifications to it for the sake of simplicity but this should be adjusted to research objectives and equally (preferably) doable in Python. 
1. If there are more than one postcode district for a location, I have kept the 1st one listed (one can work out the largest area etc to use the corresponding postcode district etc).
2. If there were more than 1 location listed in each cell of locations, I added these as seperate observations in the file, with the same postcode district. 
3. I have renamed the variable Postcode district to Postcodedistrict for convenience.
The only 2 columns of interest here for us are Location and Postcodedistrict. 

**Set of slides 1:** Notes for Webscraping with Python

**Set of slides 2:** Notes for Text as Data/ Natural Language Processing with Python

**Code 1:** main.py (I was bored to change the name) - urls extractor from the target website

**Code 2:** Scraper.py - scrape the paragraphs we need from the collected urls and save them

**Code 3:** textasdata1.py - does some standard run-of-the-mill NLP to our data (not very useful often in real world and in our case as well)

**Code 4:** textasdata2.py - extracts dates using regex, extracts location with training data (supervised learning - classification), maps location of unsolved murders in London

## Declarations

Could not have done this without encouragements from Brendon and Corrado. I do cheat a little in these sessions. Pre-processing of datafile 3 should be done in Python. Some codes can be more efficient (writing loops/functions/using Regex etc). All errors/mistakes are mine and I will highly appreciate if you reach out to me if you spot any!

## Sources

