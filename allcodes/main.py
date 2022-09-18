import csv
import time
# need the below imports to work with Explicit wait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from numpy import random
from time import sleep

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')

browser = webdriver.Firefox()
tsleep = random.uniform(1, 7)
baseurl = 'https://www.murdermap.co.uk/unsolved/'

with open('YOUR DIRECTORY/url_collector.csv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, delimiter=",")
    browser.get(baseurl)
    time.sleep(1)
    browser.maximize_window()
    time.sleep(3)
    WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[starts-with(@id, 'post-3327')]/div/div[2]//descendant::article")))
    elems = browser.find_elements(By.XPATH, ".//*[starts-with(@id, 'post-3327')]/div/div[2]//descendant::a")
    sleep(tsleep)
    for a in elems:
        hrefs = a.get_attribute('href')
        writer.writerow([hrefs])
f.close()
browser.quit()

