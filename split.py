import csv
import os, sys
import argparse
import random


def split(src_file, des_file, number):
    random.seed(3)
    with open(src_file + ".csv", 'rb') as csvfile:
        
        reader = csv.DictReader(csvfile)

        select = [i for i in xrange(number)]
        
        data = list(reader)
        #print len(data)
        for i in xrange(number, len(data)):
            ran = random.randint(0, i)
            if ran < number:
                select[ran] = i

        selected = []
        unselected = []
        i = 0
        for row in data:
            if i in select:
                selected.append(row)
            else:
                unselected.append(row)
            i += 1

        save_csv(des_file, selected, reader.fieldnames)
        save_csv(des_file+"_remain", unselected, reader.fieldnames)
        

def save_csv(name, data, header):
    # name new file with current data
    csvfile = file(name + ".csv", 'wb')
    writer = csv.DictWriter(csvfile, fieldnames=header)

    writer.writeheader()
    writer.writerows(data)
    csvfile.close()



def main(args):

    src_file = args.src_csv
    des_file = args.des_csv
    number = args.number

    split(src_file, des_file, number)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--src_csv',
                        help='File containing raw data.',
                        type=str,
                        default='')
    parser.add_argument('--des_csv',
                        help='File containing random generated data.',
                        type=str,
                        default='')
    parser.add_argument('--number',
                        help='Number of random generated data.',
                        type=int,
                        default=0)

    args = parser.parse_args()
    main(args)