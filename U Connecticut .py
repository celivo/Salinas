#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

URL = "https://catalog.uconn.edu/directory-of-courses/"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
    p =  re.search(r'courses\/course\/([^"]+)', str(link))
    if p:
        departments.append("https://catalog.uconn.edu/directory-of-" + p.group(0))
departments_of_interest = [departments[3], departments[4], departments[104], departments[105]]


filename = "U Connecticut" + ".csv"

csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Department", "CCN", "Title",  "Desc", "Graduate", "Format", "Lab", "Year"])
keywords = ["agri", "agricultural", "food", "animal"]
    
for dep in departments_of_interest:
    URL = dep
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    courses = soup.findAll(class_="single-course single-subject")
    department = soup.findAll(class_="breadcrumbs")
    department = re.findall(r'(\w*) Courses', str(department))[0]
    for course in courses:
        title = re.findall(r'<h3>(.+?)</h3>', str(course))[0]
        ccn = re.findall(r'[0-9]*\w?\.', str(title))[0]
        ccn = ccn.replace('.', '')
        title = re.findall(r'\. (.*)', str(title))[0]
        desc = course.find(class_="description").text
        graduate = None
        format = None
        lab = None
        year = "2020-2021"

        
        
        for key in keywords:
            if (re.search(key, title, flags=re.IGNORECASE) or 
                re.search(key, desc, flags=re.IGNORECASE)):
                csv_writer.writerow([department, ccn, title, desc, graduate, format, lab, year])


# In[5]:


data = pd.read_csv('U Connecticut.csv')
data


# In[ ]:




