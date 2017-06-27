import requests
import sys
import csv
import configparser
import logging
import xml.etree.ElementTree as ET

def read_notes():
    


logging.basicConfig(filename='status.log',level=logging.DEBUG)
config = configparser.ConfigParser()
config.read(sys.argv[1])

paid_notes = sys.argv[2]
read_notes(paid_notes)
