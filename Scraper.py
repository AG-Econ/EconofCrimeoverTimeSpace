import csv
import time
# need the below imports to work with Explicit wait
from selenium import webdriver
from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from numpy import random
from time import sleep

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
tsleep = random.uniform(1, 7)
browser = webdriver.Firefox()
with open("/Users/ag917/Dropbox/python_webscrape/url_collector.csv") as p:
    with open('/Users/ag917/Dropbox/python_webscrape/datafile1.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["Year", "Text1", "Text2"])
        for link in p:
            url = link.strip()
            years = [d for d in url if d.isdigit()]
            year = ''.join(years)
            print(year)
            browser.get(url)
            time.sleep(3)
            browser.maximize_window()
            sleep(tsleep)
            WebDriverWait(browser, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//*[starts-with(@class, 'wp-container-')]")))
            try:
                browser.find_element(By.CSS_SELECTOR, ".entry-content > hr:nth-child(3)")
                print("TYPE 1")
                time.sleep(3)
                try:
                    t1 = browser.find_elements(By.XPATH,
                                               "//*[starts-with(@class, 'wp-block-separator')]//following-sibling::p[1]")
                    sleep(tsleep)
                    t2 = browser.find_elements(By.XPATH,
                                               "//*[starts-with(@class, 'wp-block-separator')]//following-sibling::p[2]")
                    for m, s in zip(t1, t2):
                        # print(f.text, s.text)
                        writer.writerow([year] + [m.text] + [s.text])
                except:
                    print("I have run in some other issue")
            except (NoSuchElementException, StaleElementReferenceException):
                try:
                    browser.find_element(By.XPATH, "//*[starts-with(@class, 'wp-block-separator')]")
                    print("TYPE 2")
                    try:
                        t3 = browser.find_elements(By.XPATH,
                                                   "//*[starts-with(@class, 'wp-block-separator')]//following-sibling::p[1]")
                        t4 = browser.find_elements(By.XPATH,
                                                   "//*[starts-with(@class, 'wp-block-separator')]//following-sibling::p[2]")
                        for w, x in zip(t3, t4):
                            writer.writerow([year] + [w.text] + [x.text])
                    except (NoSuchElementException, StaleElementReferenceException):
                        t3 = browser.find_elements(By.XPATH,
                                                   "//*[starts-with(@class, 'wp-block-separator')]//following-sibling::p[1]")
                        writer.writerow([year] + [t3.text])
                    sleep(tsleep)
                    t1 = browser.find_element(By.CSS_SELECTOR, ".entry-content > p:nth-child(3)")
                    try:
                        t2 = browser.find_element(By.CSS_SELECTOR, ".entry-content > p:nth-child(4)")
                        writer.writerow([year] + [t1.text] + [t2.text])
                    except (NoSuchElementException, StaleElementReferenceException):
                        writer.writerow([year] + [t1.text])
                except (NoSuchElementException, StaleElementReferenceException):
                    sleep(tsleep)
                    print("TYPE 3")
                    t = browser.find_elements(By.XPATH,
                                              "//*[starts-with(@class, 'wp-container')]//following-sibling::p")
                    for txt in t:
                        writer.writerow([year] + [txt.text])

    f.close()
p.close()
browser.quit()
