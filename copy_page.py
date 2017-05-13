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


"""
Introduction:
    Command-line application for youtube crawler.

For more information, see the README.md .
"""



NUM_TO_COUNT = 2

reload(sys)
sys.setdefaultencoding('utf8')

# Class for basic information crawler
class Info_Spider(object):
    def __init__(self, filename):
        super(Info_Spider, self).__init__()
        self.__start_url = []
        self.__names = []

        for line in open(filename):
            self.__start_url.append(line)
    def advisor_crawl(self):
        driver = webdriver.Chrome()
        c = 0
        for url in self.__start_url:
            driver.get(url)

            for i in xrange(1, NUM_TO_COUNT/2 + 1):
                shops = driver.find_elements_by_class_name("property_title")
                for j in xrange(len(shops)):
                    if shops[j].text in self.__names:
                        continue
                        
                    self.__names.append(shops[j].text)
                    d_url = shops[j].get_attribute("href")
                    driver.get(d_url)
                    c += 1
                    tar = open('advisor/'+str(c)+".html", 'w')
                    tar.write(driver.page_source)
                    tar.close()
                    driver.back()
                    shops = driver.find_elements_by_class_name("property_title")

                next_page = driver.find_elements_by_xpath("//a[contains(@class, 'pageNum taLnk')]")
                has_next = False
                next_url = ""
                for j in xrange(len(next_page)):
                    if i + 1 == int(next_page[j].text):
                        next_url = next_page[j].get_attribute('href')
                        has_next = True
                        break
                if not has_next:
                    break
                else:
                    driver.get(next_url)

    def yelp_crawl(self):
        driver = webdriver.Chrome()
        c = 0
        for url in self.__start_url:
            driver.get(url)

            for i in xrange(1, NUM_TO_COUNT + 1):
                c += 1
                tar = open('yelp/'+str(c)+".html", 'w')
                tar.write(driver.page_source)
                tar.close()
                next_page = driver.find_elements_by_xpath(".//a[contains(@class, 'available-number pagination-links_anchor')]")
                has_next = False
                next_url = ""
                for j in xrange(len(next_page)):
                    if i + 1 == int(next_page[j].text):
                        next_url = next_page[j].get_attribute('href')
                        has_next = True
                        break
                if not has_next:
                    break
                else:
                    driver.get(next_url)

# change 10,000 to 10000
def change_num_type(ori_num):
    ori_num = ori_num.replace(',','')
    return int(ori_num)

def main(args):

    crawl_yelp = args.yelp
    url_file = args.urls

    if crawl_yelp:
        spidey = Info_Spider(url_file)
        spidey.yelp_crawl()
    else:
        spidey = Info_Spider(url_file)
        spidey.advisor_crawl()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--urls',
                        help='File containing urls to crawl.',
                        type=str,
                        default='')
    parser.add_argument('--yelp',
                        help='Crawl yelp.',
                        type=bool,
                        default='')

    args = parser.parse_args()
    main(args)