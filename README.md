# Summer School Day 2: The Economics of Crime over Time and Space: Theory, Practice and Applications

## Overview

These sessions aim to give knowhow of (context-specific)
1. scraping data from dynamic websites (session 1), 
2. working with unstructured text (session 2). 

We will use the following website to get our data and work with it: https://www.murdermap.co.uk/. There is a lot of ground to cover, so I will be at places skipping some basic steps (the goal is the breadth and not depth). It might be difficult to follow with running all the codes unless you are already quite comfortable with Python. But if that's not the case, I am happy to answer questions over email. I will run all the codes and explain the process, so if you can't run the codes on the day that should not affect your understanding too much. This readme file gives instructions and descriptions for all files/slides/codes. 

## Instructions

I'll be working with Python 3.10. If you haven't used Python before, I recommend PyCharm IDE (integrated development environment). It's available here (community version): https://www.jetbrains.com/pycharm/download/. If you are not familiar with Pycharm, please open it and create a new project in your desired location and select the relevant python version. Then copy all the codes in the project folder and data files 4 & 5 (description below) in that folder. If you are only running codes in session 2 then you will also need to copy data files 1 & 2. If you have multiple versions of Python in your machine, you might want to create a virtual environment for this project (instructions to start with: https://stackoverflow.com/questions/62428732/two-versions-of-python-in-one-computer).

We will use Google Chrome to inspect the HTML for scraping but will use the Firefox driver for the actual web scraping part. You might prefer to use other drivers like Google (in that case you will need to rectify the web.browser command in the urlcollector.py). 

For ethical reasons (and practical reasons of not overloading the target website with 30+ requests)- I suggest that you follow the talk and see me use the code for scraping to get the data in the first part. If you are interested in practicing you can do so later and I will be happy to answer further questions over email for this part.

If you want to run the scraping codes you need to have geckodriver for launching Firefox (instructions: https://selenium-python.readthedocs.io/installation.html). I have a mac and used ''brew install geckodriver'' from the terminal. You will need to download the system-specific geckodriver (https://github.com/mozilla/geckodriver/releases). 

For the second part, I have already provided the data (raw_data.csv) I obtained with the scraping code and you can follow along by running the code with me if you wish.

You need to change the directory paths in the code files accordingly (where there is YOUR DIRECTORY in the codes).

## Installing packages

There are a few packages we'll use that you need to install. Some basic general-use Python libraries you'll need to install (or probably already have):
* re 
* os
* sys
* csv
* time
* numpy
* pandas
* matplotlib
* statsmodels

Then some more scraping; natural language processing or machine learning; mapping specific packages:
* selenium
* spacy (check https://spacy.io/usage for relevant installations)
* sklearn
* nltk
* geopy
* folium

The code files have the import commands as well. 

**Sidenotes (irrelevant if you already know and use Pycharm):** If you're using PyCharm, in the bottom-right corner of the screen it will say something like "Python 3.10" to tell you which Python interpreter PyCharm is using. If you click on this, then on "Interpreter Settings" in the menu that pops up, it will list the packages installed. At the bottom (or top depending on the system) of this list, there will be a "+" symbol that allows you to install new packages. If you click the "+" button, it will bring up a list of available packages, and you can search by name for the packages listed above, and it will automatically install for you.

Pycharm's added advantage (for me) is that if there is an import command for which the package is not installed, the import command comes with a red underline, and right-clicking on that will give you options to install packages as well. Also, Pycharm can streamline optimizing import as well. 

## File descriptions

**Datafile 1:** url_collector.csv - this file contains the specific URLs from which we scrape the intended data (output from main.py, and used as input in Scraper.py: session 1)

**Datafile 2:** raw_data.csv - this file contains the scraped data obtained from the Scraper.py code below (output from session 1). This is also the input file for us to work with in session 2. 

**Datafile 3:** raw_data_2.csv - this file contains the intermediate file obtained from textasdata1.py and the input of textasdata2.py

**Datafile 4:** london_places.csv - this data I obtained from Wikipedia (https://en.wikipedia.org/wiki/List_of_areas_of_London). I have done 3 modifications to it for the sake of simplicity but this should be adjusted to research objectives and equally (preferably) doable in Python. 
1. If there are multiple postcode districts for a location, I kept the 1st one listed (one can work out the largest area, etc to use the corresponding postcode district, etc).
2. If there were more than one location listed in each cell of locations (like 'Barnet (also Chipping Barnet, High Barnet)'), I added these as separate observations in the file, with the same postcode district. 
3. I have renamed the variable Postcode district to Postcodedistrict for convenience.
The only 2 columns of interest here for us are Location and Postcodedistrict. 

**Datafile 5:** postcode_outcodes.csv - this is for the latitude and longitude mapping from postcode districts. I downloaded the Outcode Area Postcodes csv from https://www.freemaptools.com/download-uk-postcode-lat-lng.htm and just adjusted the name with '-' to '_'.

**Session 1:**

  - **Set of slides 1:** Notes for Web scraping with Python

  - **Code 1:** urlcollector.py - extracts URLS from the target website

  - **Code 2:** Scraper.py - scrapes the paragraphs we need using the collected URLs and saves them

**Session 2:**

  - **Set of slides 2:** Notes for Text as Data/ Natural Language Processing with Python
  
  - **Code 3:** textasdata1.py - does some standard run-of-the-mill NLP to our data (can be very useful often in other data even if not necessarily for our  case, given our goal)

  - **Code 4:** textasdata2.py - extracts dates using regex, extracts location with training data (supervised learning - classification), maps location of unsolved murders in London

## Declarations

Could not have done this without encouragement from Brendon and Corrado. I do cheat a little in these sessions. Pre-processing of datafile 4 should be done in Python. Some codes can be more efficient (writing loops/functions/using Regex etc). All errors/mistakes are mine and in case you spot any, I will highly appreciate it if you reach out to me!

## Sources

At the end of the set of slides 2
