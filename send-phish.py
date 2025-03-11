#!/bin/python3
'''
A simple script to read a phish URL and brandname and feed it 
into the APWG UBL via the API.
'''

import dateutil.parser
import requests, datetime, dateutil
from config import CONFIG;

def insert(record):
    """
    Sends a POST request to an API endpoint to add a cryptocurrency address document.
    Prints the response content in a human-readable format.
    """
    try:
        lf = open(CONFIG['LOG_FILE_PHISH'], 'a')
    except Exception as e:
        print("File broke: " + e)
        exit(4)
    api_url = CONFIG['api_url_phish']
    headers = {
        "Authorization": f"Bearer " + CONFIG['api'],
        "Content-Type": "application/json",  # Specify content type for the request
    }
    try:
        resp = requests.post( api_url, json=record, headers=headers )
    except Exception as es1:
        pass
    print("API Response:")
    print(str(resp.status_code) + ' - ' + resp.text)
    lf.write("url:" + record['url'] + ' Response: ' + str(resp.status_code) + ' id: ' + resp.text)
    lf.close()
    return 

tz = [ 'UTC', 'EST', 'EDT' ]

def main():

    url = input("Please enter the phishing URL:")
    brand = input("Brand:")
    date = input("Recd Date:")
    pick1 = input(" 0-UTC, 1-EST, 2-EDT :")
    dateFormat = "%a %m/%d/%Y %H:%M %p %Z"
    newDate = date + ' ' + tz[int(pick1)]
    try:
        goodDate = datetime.datetime.strptime(newDate, dateFormat)
    except ValueError:
        #dateutil.parser.parse("3:21 pm")
        exit(13)
    record = {
        "brand": brand,
        "url": url,
        "confidence": 100,
        "discoveredAt": int(goodDate.timestamp())
    }
    insert(record)
    pass


if __name__ == "__main__":
    main()