#!/usr/bin/env python
# coding: utf-8

# In[23]:


import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

URL = "http://guide.berkeley.edu/courses/"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
    p =  re.search(r'\/courses\/([^"]+)', str(link))

    if p:
        departments.append("http://guide.berkeley.edu" + p.group(0))

departments_of_interest = [departments[2], departments[6], departments[7], departments[8], departments[18]]

filename = "berkeley" + ".csv"

csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Department", "CCN", "Title",  "Desc", "Graduate", "Format", "Lab", "Year"])
keywords = ["agri", "agricultural", "food", "animal"]

for dep in departments_of_interest:
    URL = dep
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    courses = soup.findAll(class_="courseblock")
    department = soup.findAll(class_='page-header')[0]
    department = re.findall(r'\>(.*) \(', str(department))[0]
    for course in courses:
        title = course.find(class_='title').text
        desc = course.find(class_="descshow").text
        ccn = course.find(class_= 'code')
        ccn = int(re.findall('[0-9]+', str(ccn))[0])
        graduate = None
        if ccn >= 200:
            graduate = True
        else:
            graduate = False
            
        lab = False
        if "Lab" or "LAB" or "lab" in desc:
            lab = True
        else:
            lab = False
            
        year = "2020-2021"
        
        for key in keywords:
            if (re.search(key, title, flags=re.IGNORECASE) or 
                re.search(key, desc, flags=re.IGNORECASE)):
                csv_writer.writerow([department, ccn, title, desc, graduate, None, lab, year])


# In[24]:


data = pd.read_csv('berkeley.csv')
data


# In[ ]:




