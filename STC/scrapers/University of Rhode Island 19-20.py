import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.request
import csv

URL = 'https://web.uri.edu/catalog/course-descriptions/'
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('li')

#filename = "University_of_Rhode_Island_Sample.csv"
#csv_writer = csv.writer(open(filename, 'w'))
#csv_writer.writerow(["Course Catalogue Number", "Department Name", "Course Name",
# "Course Description", "Graduate/Undergraduate", "Format", "Lab", 
# "Academic Catalogue Year", "Food Systems", "Food Justice/Equity",
# "Critical Pedagogy"])
FS_keys = ["agri", "food", "animal"]
#FJ_keys = ["conservation", "ethical"]
#CP_keys = ["communication", "discussion"]
year = "2019-2020"
lab = None
#FS = False
#FJ = False
#CP = False

courses = soup.findAll(class_="showResult")