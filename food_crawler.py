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



NUM_TO_COUNT = 10

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

        for line in open(filename):
            self.__start_url.append(line)

    def advisor_crawl(self):
        driver = webdriver.Chrome()
        for url in self.__start_url:
            driver.get(url)

            for i in xrange(i, NUM_TO_COUNT/2 + 1):
                shops = diver.find_elements_by_class_name("property_title")
                for shop in shops:
                    self.__names.append(shop.text)
                    d_url = shop.get_attribute("href")
                    driver.get(d_url)
                    star = driver.find_elements_by_class_name("sprite-rating_rr_fill rating_rr_fill")
                    self.__stars.append(star[0].get_attribute("content"))

                    price = driver.find_elements_by_class_name("detail first price_rating separator")
                    self.__money.append(price[0].text)

                    review = driver.find_elements_by_xpath("//div[contains(@class, 'rs rating')]/a")
                    self.__reviews.append(review[0].get_attribute("content"))

                    addr = driver.find_elements_by_class_name("postalCode")
                    self.__addrs.append(addr[0].text)

                    phone = driver.find_elements_by_class_name("fl phoneNumber")
                    self.__phones.append(phone[0].text)

                    driver.back()

                next_page = driver.find_elements_by_class_name("pageNum taLnk")
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

                self.save_csv("yelp")

    def yelp_crawl(self):
        driver = webdriver.Chrome()
        for url in self.__start_url:
            driver.get(url)

            for i in xrange(i, NUM_TO_COUNT + 1):
                # shops = driver.find_elements_by_class_name("biz-name js-analytics-click")
                names = driver.find_elements_by_xpath("//a[contains(@class, 'biz-name js-analytics-click')]/span")
                for name in names:
                    self.__names.append(name.text)

                stars = drive.find_elements_by_class_name("star-img")
                for star in stars:
                    star_s = star.split(" ")
                    self.__stars.append(start_s[0])

                reviews = driver.find_elements_by_class_name("biz-name js-analytics-click")
                for review in reviews:
                    review_s = review.text.split(" ")
                    self.__reviews.append(review_s[0])

                prices = driver.find_elements_by_class_name("business-attribute price-range")
                for price in prices:
                    self.__money.append(price.text)

                phones = driver.find_elements_by_class_name("biz-phone")
                for phone in phones:
                    self.__phones.append(phone.text)

                addrs = driver.find_elements_by_xpath(("//div[contains(@class, 'secondary-attributes')]/address"))
                for addr in addrs:
                    code = addr.text.split(" ")
                    self.__addrs.append(addr[-1])

                next_page = driver.find_elements_by_class_name("available-number pagination-links_anchor")
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

    crawl_yelp = args.website

    if crawl_yelp:
        spidey = Info_Spider(url_file)
        spidey.yelp_crawl()
    else:
        spidey = Info_Spider(url_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--website',
                        help='File containing urls to crawl.',
                        type=str,
                        default='')

    args = parser.parse_args()
    main(args)
