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
    return get_base_url() + '/acq/po-lines/' + id + '?apikey=' + get_key()

# Returns XML for POL if successful GET request
def get_request(url):
    results = requests.get(url)
    if results.status_code != 200:
        logging.info('Failed to get results for: ' + url)
        return None
    else:
        return_data = ET.fromstring(results.content)
        return return_data

# Adds PAID field labels to each field
def populate_data(r):
    return_data = ''
    return_data = return_data +  'Paid Date: '  + r[0].strip('"')
    return_data = return_data +  ' | Invoice Date: ' + r[1].strip('"')
    return_data = return_data +  ' | Invoice Num: ' + r[2].strip('"')
    return_data = return_data +  ' | Amount Paid: ' + r[3].strip('"')
    return_data = return_data +  ' | Voucher Num: ' + r[4].strip('"')
    return_data = return_data +  ' | Copies: ' + r[5].strip('"')
    return_data = return_data +  ' | Sub From: ' + r[6].strip('"')
    return_data = return_data +  ' | Sub To: ' + r[7].strip('"')
    for x in range(8,len(r)):
        return_data = return_data +  ' | Note: ' + r[x].replace("\\", "").strip('"')
    return return_data

# Parses PAID fields into format expected in POL notes
def parse_row(row):
    notes_array = []
    notes_array.append(row[0].split(',')[0])
    notes_array.append('BLOC: ' + row[0].split(',')[1].strip('"'))
    i = 0
    first = True
    for r in row:
        # Each r contains a PAID note field
        r = r.split(',')
        if first: # first line contains one extra field, remove it from parsing
            r = r[2:]
            first = False
        if len(r) > 2: # Checking to see if there is PAID data in the incoming data
            return_data = populate_data(r)
            notes_array.append(return_data)
    return notes_array

# posts updated POL to Alma API
def post_pol(url,xml):
    headers = {"Content-Type": "application/xml"}
    r = requests.put(url,data=ET.tostring(xml),headers=headers)
    if r.status_code != 200:
        logging.info('Failed to post: ' + url)
    else:
        logging.info('Success update for: ' + url)

# Iterates through each note, and creates a note element
def add_pol_note(notes):
    id = notes[0]
    del notes[0]
    url = get_pol_url(id)
    print (url)
    xml = get_request(url)
    if xml is not None:
        notes_node = xml.find("notes")
        for n in notes:
            print (n)
            sub = ET.SubElement(notes_node,'note')
            note_text = ET.SubElement(sub, 'note_text')
            note_text.text = n
        post_pol(url,xml)

# Reads each line of the input file
def read_notes(notes):
    f  = open(notes,'rt')
    try:
        reader = csv.reader(f,delimiter=';')
        header = next(reader)
        for row in reader:
            parsed_notes = parse_row(row)
        #    add_pol_note(parsed_notes)
    finally:
        f.close()

logging.basicConfig(filename='status.log',level=logging.DEBUG)
config = configparser.ConfigParser()
config.read(sys.argv[1])

paid_notes = sys.argv[2]
read_notes(paid_notes)
