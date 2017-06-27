import requests
import sys
import csv
import configparser
import logging
import re
import xml.etree.ElementTree as ET

# Returns the API key
def get_key():
    return config.get('Params', 'apikey')

# Returns the Alma API base URL
def get_base_url():
    return config.get('Params', 'baseurl')

def get_pol_url(id):
    return get_base_url() + '/acq/po-lines/' + id + '?apiey=' + get_key()

# Reads each line of the input file
def read_notes(notes):
    f  = open(notes,'rt')
    try:
        reader = csv.reader(f,delimiter=';')
        header = next(reader)
        for row in reader:
            parse_row(row)
    finally:
        f.close()


def populate_data(r):
    return_data = ''
    return_data = return_data +  'Paid Date: '  + r[0].strip('"')
    return_data = return_data +  '| Invoice Date: ' + r[1].strip('"')
    return_data = return_data + '| Invoice Num: ' + r[2].strip('"')
    return_data = return_data +  '| Amount Paid: ' + r[3].strip('"')
    return_data = return_data +  ' | Voucher Num: ' + r[4].strip('"')
    return_data = return_data +  ' | Copies: ' + r[5].strip('"')
    return_data = return_data + ' | Sub From: ' + r[6].strip('"')
    return_data = return_data +  ' | Sub To: ' + r[7].strip('"')
    for x in range(8,len(r)):
        return_data = return_data +  ' | Note: ' + r[x].replace("\\", "")
    return return_data

def parse_row(row):
    notes_array = []
    id = row[0].split(',')[0]
    first = True
    for r in row:
        print (r)
        r = r.split(',')
        # first line contains one extra field, remove it from parsing
        if first:
            r = r[1:]
            first = False
        return_data = populate_data(r)
        print (return_data)
        notes_array.append(return_data)



logging.basicConfig(filename='status.log',level=logging.DEBUG)
config = configparser.ConfigParser()
config.read(sys.argv[1])

paid_notes = sys.argv[2]
read_notes(paid_notes)
