#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

URL = "https://catalog.uark.edu/undergraduatecatalog/coursesofinstruction/"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
    p =  re.search(r'\/undergraduatecatalog\/coursesofinstruction\/([^"]+)', str(link))

    if p:
        departments.append("https://catalog.uark.edu" + p.group(0))

departments_of_interest = [departments[3], departments[4], departments[5], departments[6], departments[7]]

filename = "arkansas" + ".csv"

csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Department", "CCN", "Title",  "Desc", "Graduate", "Format", "Lab", "Year"])
keywords = ["agri", "agricultural", "food", "animal"]

for dep in departments_of_interest:
    URL = dep
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    courses = soup.findAll(class_="courseblock")
    department = soup.title
    department = re.findall('\>(.*)\ &', str(department))[0]
    for course in courses:
        intro = course.find(class_="courseblocktitle").text
        splt = intro.split(".")
        title = splt[0] + splt[1]
        desc = course.find(class_="courseblockdesc").text
        ccn = re.findall('[0-9]+\w?', str(title))[0]
        graduate = "U"
        year = "2020-2021"
        for key in keywords:
            if (re.search(key, title, flags=re.IGNORECASE) or 
                re.search(key, desc, flags=re.IGNORECASE)):
                csv_writer.writerow([department, ccn, title, desc, graduate, None, None, year])


# In[6]:


data = pd.read_csv('arkansas.csv')
data


# In[ ]:




