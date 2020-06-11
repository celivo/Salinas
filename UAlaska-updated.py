#!/usr/bin/env python
# coding: utf-8

# In[11]:


import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

URL = "https://catalog.uaa.alaska.edu/coursedescriptions/"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
    p =  re.search(r'\/coursedescriptions\/([^"]+)', str(link))
    if p:
        departments.append("https://catalog.uaa.alaska.edu" + p.group(0))
departments_of_interest = [departments[2], departments[7], departments[17], departments[20], departments[43]]

filename = "Ualaska" + ".csv"

csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Department", "CCN", "Title", "Desc", 'Graduate', 'Format', 'Lab', "Year"])
keywords = ["agri", "agricultural", "food", "animal"]
for dep in departments_of_interest:
    URL = dep
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    courses = soup.findAll(class_="courseblock")
    department = soup.find(class_="page-title")
    department = re.findall('\>(.*)\<', str(department))[0]
    department = department.replace(' &amp;', '')
    
    for course in courses:
        intro = course.find(class_="courseblocktitle").text
        if "  " in intro:
            lst = intro.split("  ")
            title = lst[0]
            credits = lst[1]
        ccn = re.findall('\w?[0-9]+\w?', str(title))[0]
        
        desc = course.find(class_="courseblockdesc").text
        year = "2019-2020"

        for key in keywords: #filtered
            if (re.search(key, title, flags=re.IGNORECASE) or 
                re.search(key, desc, flags=re.IGNORECASE)):
                csv_writer.writerow([department, ccn, title, desc, None, None, None, year])


# In[12]:


data = pd.read_csv('Ualaska.csv')
data


# In[ ]:




