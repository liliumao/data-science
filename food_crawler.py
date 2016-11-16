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



NUM_TO_COUNT = 100

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
        self.__postal_codes = []
        self.__phones = []
        self.__addrs = []


        for line in open(filename):
            self.__start_url.append(line)
    def advisor_crawl(self):
        driver = webdriver.Chrome()
        for url in self.__start_url:
            driver.get(url)

            for i in xrange(1, NUM_TO_COUNT):
                shops = driver.find_elements_by_class_name("property_title")
                for j in xrange(len(shops)):
                    if shops[j].text in self.__names:
                        continue

                    self.__names.append(shops[j].text)
                    d_url = shops[j].get_attribute("href")
                    driver.get(d_url)
                    star = driver.find_elements_by_xpath("//img[contains(@class, 'sprite-rating_rr_fill rating_rr_fill')]")
                    if star:
                        self.__stars.append(float(star[0].get_attribute("content")))
                    else:
                        self.__stars.append(-1)

                    price = driver.find_elements_by_xpath("//div[contains(@class, 'detail first price_rating separator')]")
                    if price:
                        self.__money.append(price[0].text)
                    else:
                        self.__money.append("")

                    review = driver.find_elements_by_xpath("//div[contains(@class, 'rs rating')]/a")
                    if review:
                        self.__reviews.append(int(review[0].get_attribute("content")))
                    else:
                        self.__reviews.append(-1)

                    postal = driver.find_elements_by_xpath("//span[contains(@property, 'postalCode')]")
                    if postal:
                        self.__postal_codes.append(postal[0].text)
                    else:
                        self.__postal_codes.append("")

                    addr = driver.find_elements_by_xpath("//span[contains(@property, 'streetAddress')]")
                    if addr:
                        self.__addrs.append(addr[0].text)
                    else:
                        self.__addrs.append("")

                    phone = driver.find_elements_by_xpath("//div[contains(@class, 'fl phoneNumber')]")
                    if phone:
                        self.__phones.append(phone[0].text)
                    else:
                        self.__phones.append("")

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
                    if stars:
                        star_s = stars[0].get_attribute("title").split(" ")
                        self.__stars.append(float(star_s[0]))
                    else:
                        self.__stars.append(-1)

                    reviews = div.find_elements_by_xpath(".//span[contains(@class, 'review-count rating-qualifier')]")
                    if reviews:
                        review_s = reviews[0].text.split(" ")
                        self.__reviews.append(int(review_s[0]))
                    else:
                        self.__reviews.append(-1)

                    prices = div.find_elements_by_xpath(".//span[contains(@class, 'business-attribute price-range')]")
                    if prices:
                        self.__money.append(prices[0].text)
                    else:
                        self.__money.append("")

                    phones = div.find_elements_by_class_name("biz-phone")
                    if phones:
                        self.__phones.append(phones[0].text)
                    else:
                        self.__phones.append("")

                    addrs = div.find_elements_by_xpath((".//div[contains(@class, 'secondary-attributes')]/address"))
                    if addrs:
                        addr = addrs[0].text.split('\n')
                        code = addr[1].split(" ")
                        self.__postal_codes.append(code[-1])
                        self.__addrs.append(addr[0])
                    else:
                        self.__postal_codes.append("")
                        self.__addrs.append("")

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

        self.save_csv("yelp")

    def save_csv(self, name):
        # name new file with current data
        csvfile = file(name + ".csv", 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(["shop name", "postal code", "phone number", "star", "price", "number of reviews", "street address"])
        data = []
        for i in range(len(self.__names)):
            line = (self.__names[i], self.__postal_codes[i], self.__phones[i],
                    self.__stars[i], self.__money[i], self.__reviews[i], self.__addrs[i])
            data.append(line)

        writer.writerows(data)
        csvfile.close()

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
