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
import time


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
        self.__reviews = []
        self.__stars = []
        self.__money = []
        self.__names = []
        self.__addrs = []
        self.__phones = []

        # for line in open(filename):
        #     self.__start_url.append(line)

    def advisor_crawl(self):
        driver = webdriver.Chrome()

        self.__start_url.append("https://www.tripadvisor.com/Restaurants-g32655-Los_Angeles_California.html")
        for url in self.__start_url:
            driver.get(url)

            for i in xrange(1, NUM_TO_COUNT/2 + 1):
                shops = driver.find_elements_by_class_name("property_title")
                for j in xrange(0, 2):
                    self.__names.append(shops[j].text)
                    d_url = shops[j].get_attribute("href")
                    driver.get(d_url)
                    star = driver.find_elements_by_xpath("//img[contains(@class, 'sprite-rating_rr_fill rating_rr_fill')]")
                    self.__stars.append(star[0].get_attribute("content"))

                    price = driver.find_elements_by_xpath("//div[contains(@class, 'detail first price_rating separator')]")
                    self.__money.append(price[0].text)

                    review = driver.find_elements_by_xpath("//div[contains(@class, 'rs rating')]/a")
                    self.__reviews.append(review[0].get_attribute("content"))

                    addr = driver.find_elements_by_xpath("//span[contains(@property, 'postalCode')]")
                    self.__addrs.append(addr[0].text)

                    phone = driver.find_elements_by_xpath("//div[contains(@class, 'fl phoneNumber')]")
                    self.__phones.append(phone[0].text)

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

        self.save_csv("advisor")

    def yelp_crawl(self):
        driver = webdriver.Chrome()
        self.__start_url.append("https://www.yelp.com/search?find_loc=Los+Angeles,+CA,+USA&start=0&cflt=food")
        for url in self.__start_url:
            driver.get(url)

            for i in xrange(1, NUM_TO_COUNT + 1):
                divs = driver.find_elements_by_class_name("biz-listing-large")
                for div in divs:
                    # shops = driver.find_elements_by_class_name("biz-name js-analytics-click")
                    names = div.find_elements_by_xpath(".//a[contains(@class, 'biz-name js-analytics-click')]/span")
                    for name in names:
                        self.__names.append(name.text)

                    stars = div.find_elements_by_class_name("star-img")
                    for star in stars:
                        star_s = star.get_attribute("title").split(" ")
                        self.__stars.append(star_s[0])

                    reviews = div.find_elements_by_xpath(".//span[contains(@class, 'review-count rating-qualifier')]")
                    for review in reviews:
                        review_s = review.text.split(" ")
                        self.__reviews.append(review_s[0])

                    prices = div.find_elements_by_xpath(".//span[contains(@class, 'business-attribute price-range')]")
                    for price in prices:
                        self.__money.append(price.text)

                    phones = div.find_elements_by_class_name("biz-phone")
                    for phone in phones:
                        self.__phones.append(phone.text)

                    addrs = div.find_elements_by_xpath((".//div[contains(@class, 'secondary-attributes')]/address"))
                    for addr in addrs:
                        code = addr.text.split(" ")
                        self.__addrs.append(code[-1])

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

        print len(self.__names)
        print len(self.__addrs)
        print len(self.__phones)
        print len(self.__stars)
        print len(self.__money)
        print len(self.__reviews)
        self.save_csv("yelp")

    def save_csv(self, name):
        # name new file with current data
        csvfile = file(name + ".csv", 'wb')
        writer = csv.writer(csvfile)
        data = []
        for i in range(len(self.__names)):
            line = (self.__names[i], self.__addrs[i], self.__phones[i],
                    self.__stars[i], self.__money[i], self.__reviews[i])
            data.append(line)

        writer.writerows(data)
        csvfile.close()

# change 10,000 to 10000
def change_num_type(ori_num):
    ori_num = ori_num.replace(',','')
    return int(ori_num)

def main(args):
    crawl_yelp = args.yelp
    url_file = ""
    print crawl_yelp
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
    parser.add_argument('--yelp',
                        help='Crawl weekly subscribe.',
                        type=bool,
                        default=False)

    args = parser.parse_args()

    main(args)
