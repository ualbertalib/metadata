#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from time import sleep
import sys

def main():
    result = []
    with open('list', 'r') as f:
        urls = f.readlines()
    for url in urls:
        url = str(url).strip()
        response = requests.get(url).text
        try:
            soup = BeautifulSoup(response, 'lxml')
        except:
            print(url, 'failed to obtain response')
        try:
            metadata = soup.find('div', id="SelectedMetadata")
        except:
            print(url, 'failed to obtained metadata')
            pass
        if metadata is not None:        
            try:      
                for i in metadata.find_all('span', 'class'=='key'):
                    if 'ark:' in i.string:
                        print(url, i.string)
            except:
                print(url, 'failed to obtain ark')
                pass
        sys.stdout.flush()

        sleep(8)
            
    with open('result.csv','w') as csv:
        for line in result:
            csv.writelines(str(line) + '\n')
            
if __name__ == '__main__':
    main()

