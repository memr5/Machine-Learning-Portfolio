# Importing required Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import string

# Url of the website
base_url = 'https://babynames.extraprepare.com/'

for gender in ['boy','girl']:
    print(f"Scrapping Indian {gender}s Names")

    for initial in string.ascii_lowercase:
        # To make a request to the website
        url = base_url+f"{gender}-{initial}.php"
        request = requests.get(url)

        # To create a BeautifulSoup object with content(Source code) of the website
        soup = BeautifulSoup(request.content,'html.parser')

        with open("Names.txt",'a') as f:
            for names in soup.findAll('h3'):
                if ";" in names.text:
                    # print(names.text)
                    for name in names.text.split("; "):
                        # print(name)
                        f.write(name+"\n")
                else:
                    f.write(names.text+"\n")

            for i in soup.findAll('td',attrs={'align':'center'}):
                if "Page" in i.text:
                    for page in range(1,len(i.text[6:].split("\xa0"))-1):
                        request = requests.get(url+f"?page={page}")

                        # To create a BeautifulSoup object with content(Source code) of the website
                        soup = BeautifulSoup(request.content,'html.parser')

                        for names in soup.findAll('h3'):
                            if ";" in names.text:
                                # print(names.text)
                                for name in names.text.split("; "):
                                    # print(name)
                                    f.write(name+"\n")
                            else:
                                f.write(names.text+"\n")
                    
