#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

URL = "https://catalog.colostate.edu/general-catalog/courses-az/"
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
    p =  re.search(r'\/general-catalog\/courses-az\/([^"]+)', str(link))
    if p:
        departments.append("https://catalog.colostate.edu" + p.group(0))
        
departments_of_interest = [departments[8], departments[9], departments[10], departments[11]]

filename = "coloradostate" + ".csv"

csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Department", "CCN", "Title",  "Desc", "Graduate", "Format", "Lab", "Year"])
keywords = ["agri", "agricultural", "food", "animal"]

for dep in departments_of_interest:
    URL = dep
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    courses = soup.findAll(class_="courseblock")
    department = soup.findAll(class_="page-title")
    department = re.findall(r'>(.*)<', str(department))[0]
    for course in courses:

        intro = course.find(class_="courseblocktitle").text

        if "Credits" in intro:
            lst = intro.split("Credits")
            title = lst[0]
            credits = lst[1][1:]
            
        ccn = re.findall('[0-9]+', str(title))[0]

        dessbegin = course.find(class_="courseblockdesc").text
        desc1 = dessbegin.split("Prerequisite")[0]
        desc = desc1.split("Course Description: ")[1]
        year = "2019-2020"



        for key in keywords:
            if (key in title or key in desc):
                csv_writer.writerow([department, ccn, title, desc, None, None, None, year])


# In[6]:


data = pd.read_csv('coloradostate.csv')
data


# In[ ]:




