from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import os, sys
import argparse
import xlsxwriter
import xlrd
from urllib2 import urlopen
from io import BytesIO
import csv
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf8')

def crawl():
    driver = webdriver.Chrome()
    driver.get("https://www.yelp.com/search?find_loc=Los+Angeles,+CA,+USA&start=0&sortby=review_count&cflt=restaurants")
    addrs = driver.find_elements_by_xpath(("//div[contains(@class, 'secondary-attributes')]/address"))
    for addr in addrs:
        code = addr.text.split(" ")
        print code

crawl()
