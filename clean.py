import csv
import os, sys
import argparse


def clean(csv_file):
    data = []
    names = []
    phones = []
    cnt = 1
    with open(csv_file + ".csv", 'rb') as csvfile:
        cols = ["shop name", "postal code", "phone number", "star", "price", "number of reviews", "street address"]
        reader = csv.DictReader(csvfile)
        for row in reader:

            if len(row[cols[1]]) == 10 or len(row[cols[1]]) == 9:
                row[cols[1]] = row[cols[1]][:5]
            elif len(row[cols[1]]) != 5:
                row[cols[1]] = ""

            if len(row[cols[2]]) < 10:
                row[cols[2]] = ""
            else:
                tmp = []
                for c in row[cols[2]]:
                    if c.isdigit():
                        tmp.append(c)
                if tmp[0] == "1":
                    tmp = tmp[1:]
                if tmp[0] == "0" and tmp[1] == "0" and tmp[2] == "1":
                    tmp = tmp[3:]
                if tmp[0] == "0":
                    tmp = tmp[1:]
                if len(tmp) == 10:
                    row[cols[2]] = "".join(tmp)
                elif len(tmp) == 20:
                    row[cols[2]] = "".join(tmp[:10])
                else:
                    row[cols[2]] = ""

            if row[cols[0]] in names and row[cols[2]] in phones:
                continue
            names.append(row[cols[0]])
            phones.append(row[cols[2]])
            row["ID"] = cnt
            cnt += 1
            # print row
            data.append(row)


        save_csv(csv_file, data)

def save_csv(name, data):
    # name new file with current data
    csvfile = file(name + "_clean.csv", 'wb')
    cols = ["ID", "shop name", "postal code", "phone number", "star", "price", "number of reviews", "street address"]
    writer = csv.DictWriter(csvfile, fieldnames=cols)

    writer.writeheader()
    writer.writerows(data)
    csvfile.close()


def main(args):

    csv_file = args.csv

    clean(csv_file)

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
