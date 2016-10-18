import csv
import xlsxwriter
import xlrd
import os, sys
import argparse

def cal_missing_rate(csv_file):
    data = [[] for _ in xrange(6)]
    m_data = [0 for _ in xrange(6)]

    with open(csv_file + ".csv", 'rb') as csvfile:
        cols = ["shop name", "postal code", "phone number", "star", "price", "number of reviews"]
        reader = csv.DictReader(csvfile)
        for row in reader:
            for i in xrange(len(cols)):
                if row[cols[i]]:
                    data[i].append(row[cols[i]])
                else:
                    m_data[i] += 1

        for i in xrange(6):
            print m_data[i] / (float) (m_data[i] + len(data[i]))


def main(args):

    csv_file = args.csv

    cal_missing_rate(csv_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--csv',
                        help='File containing urls to crawl.',
                        type=str,
                        default='')

    args = parser.parse_args()
    main(args)
