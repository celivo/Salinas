import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.request
import csv

URL = 'http://catalog.ncsu.edu/undergraduate/coursedescriptions/'
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
	p =  re.search(r'\/undergraduate\/coursedescriptions\/([^"]+)', str(link))
	if p:
		departments.append("http://catalog.ncsu.edu" + p.group(0))
	
some_dep = departments[3:8]
filename = "North_Carolina_State_University_Sample.csv"
csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Course Catalogue Number", "Department Name", "Course Name",
 "Course Description", "Graduate/Undergraduate", "Format", "Lab", 
 "Academic Catalogue Year", "Food Systems", "Food Justice/Equity",
 "Critical Pedagogy"])
FS_keys = ["agri", "food", "animal"]
#FJ_keys = ["conservation", "ethical"]
#CP_keys = ["communication", "discussion"]
# Q: Does the course need to have the FS word first then filter down, or are
# they three separate groups
G_UG = "UG"
form = None
lab = None
year = "2019-2020"
#FS = False
#FJ = False
#CP = False

for dep in some_dep:
	URL = dep
	page = requests.get(URL)
	soup = BeautifulSoup(page.text, 'html.parser')

	courses = soup.findAll(class_="courseblock")
	for course in courses:
		title = course.find(class_="courseblocktitle").text
		desc = course.find(class_="courseblockdesc").text
		for key in FS_keys:
			if (re.search(key, title, flags=re.IGNORECASE) or 
				re.search(key, desc, flags=re.IGNORECASE)):
				t = re.search(r"([^\d]+)\s(\d+\w*)\s(.+)", title)
				csv_writer.writerow([t.group(2), t.group(1), t.group(3), desc, 
					G_UG, form, lab, year, None, None, None])
	time.sleep(1)