#!/usr/bin/env python
# coding: utf-8

# In[10]:


import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

URL = "https://catalog.ufl.edu/UGRD/courses/"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:

    p =  re.search(r'\/UGRD\/courses\/([^"]+)', str(link))
    if p:
        departments.append("https://catalog.ufl.edu/" + p.group(0))

departments_of_interest = [departments[5], departments[6], departments[7], departments[8]]

filename = "UFlorida" + ".csv"

csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Department", "CCN", "Title",  "Desc", "Graduate", "Format", "Lab", "Year"])
keywords = ["agri", "agricultural", "food", "animal"]

for dep in departments_of_interest:
    URL = dep
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    courses = soup.findAll(class_="courseblock courseblocktoggle")
    department = soup.findAll(class_= 'page-title')
    department = re.findall('\>(.*)\<', str(department))[0]
    
    for course in courses:
        intro = course.find(class_="courseblocktitle")
        title = intro.text
        desc = course.find(class_="courseblockdesc").text
        ccn = re.findall('[0-9]+\w?', str(title))[0]
        graduate = None
        Format = None
        Lab = None
        year = "2020-2021"
        
        for key in keywords:
            if (re.search(key, title, flags=re.IGNORECASE) or 
                re.search(key, desc, flags=re.IGNORECASE)):
                csv_writer.writerow([department, ccn, title, desc, None, None, None, year])


# In[11]:


data = pd.read_csv('UFlorida.csv')
data


# In[ ]:




