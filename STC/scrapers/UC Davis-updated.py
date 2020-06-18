#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

URL = "https://ucdavis.pubs.curricunet.com/Catalog/courses-subject-code"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
    p =  re.search(r'\/\w{3}\-([^\"]+)', str(link))
    if p:
        departments.append("https://ucdavis.pubs.curricunet.com/Catalog/" + p.group(0))

departments_of_interest = [departments[1], departments[2], departments[3], departments[5]]

filename = "Davis" + ".csv"

csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Department", "CCN", "Title",  "Desc", "Graduate", "Format", "Lab", "Year"])
keywords = ["agri", "agricultural", "food", "animal"]

for dep in departments_of_interest:
    URL = dep
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    courses = soup.findAll(class_="container-fluid course-summary-wrapper")
    department = soup.findAll(id ="page-content-wrapper")
    department = re.findall(r'<h1>(.+?)</h1>', str(department))[0]
    
    for course in courses:
        intro = course.find(class_="course-title")
        ccn = course.find(class_="course-number")
        ccn = ccn = (re.findall('[0-9]+\w?', str(ccn))[0])
        title = intro.text
        desc = course.find(class_="row course-summary-paragraph").text
        graduate = None
        Year = "2020 - 2021"
        lab = False
        if "lab" or "LAB" or "Lab" in desc:
            lab = True

        
        for key in keywords:
            if (re.search(key, title, flags=re.IGNORECASE) or 
                re.search(key, desc, flags=re.IGNORECASE)):
                csv_writer.writerow([department, ccn, title, desc, graduate, None, lab, Year])


# In[8]:


data = pd.read_csv('Davis.csv')
data


# In[ ]:




