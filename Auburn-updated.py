#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

URL = "http://bulletin.auburn.edu/coursesofinstruction/"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
    p =  re.search(r'\/coursesofinstruction\/([^"]+)', str(link))
    if p:
        departments.append("http://bulletin.auburn.edu" + p.group(0))

departments_of_interest = [departments[5], departments[6], departments[7]]

filename = "Auburn" + ".csv"

csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Department", "CCN", "Title", "Desc", "Graduate", "Format", "Lab", "Year"])
keywords = ["agri", "agricultural", "food", "animal"] # variations or no?

for dep in departments_of_interest:
    URL = dep
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    #how will classes differ across sites?
    courses = soup.findAll(class_="courses")
    department = soup.find(class_='page-title')
    department = re.findall('\>(.*)\<', str(department))[0]
    for course in courses:
        intro = course.find(class_="courseblock")
        title = soup.strong.text
        title = re.findall('\w*[^(]*', str(title))[0]
        desc = intro.text
        desc = re.search(r'\(\d-?[0-9]?\)(.+)', str(desc)).group(1)
        lab = False
        if "LAB" in desc:
            lab = True
        ccn = int(re.findall('[0-9]+', str(title))[0])
        year = "2019-2020"
        
        for key in keywords: #filtered
            if (re.search(key, title, flags=re.IGNORECASE) or 
                re.search(key, desc, flags=re.IGNORECASE)):
                csv_writer.writerow([department, ccn, title, desc, None, None, lab, year])


# In[8]:


data = pd.read_csv('Auburn.csv')
data


# In[ ]:




