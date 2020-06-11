import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.request
import csv

URL = 'http://www.uwyo.edu/registrar/university_catalog/crsdept.html'
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')
results = results[108:247]
departments = []
for link in results:
	if str(link.get('href')) != 'None':
		departments.append("http://www.uwyo.edu/registrar/university_catalog/" + str(link.get('href')))

some_dep = departments[5:8]
filename = "University_of_Wyoming_Sample.csv"
csv_writer = csv.writer(open(filename, 'w', encoding='utf-8'))
csv_writer.writerow(["Department Name", "Course Catalogue Number", "Course Name",
 "Course Description", "Graduate/Undergraduate", "Format", "Lab", 
 "Academic Catalogue Year", "Food Systems", "Food Justice/Equity",
 "Critical Pedagogy"])
FS_keys = ["agri", "food", "animal"]
#FJ_keys = ["conservation", "ethical"]
#CP_keys = ["communication", "discussion"]
year = None
form = None
#FS = False
#FJ = False
#CP = False
for dep in some_dep:
	URL = dep
	page = requests.get(URL)
	soup = BeautifulSoup(page.text, 'html.parser')
	dep_name = soup.find('h2').text
	courses = soup.findAll('p')
	usp = str(courses[2])
	if not re.search(r'USP Codes are listed in', usp):
		courses = courses[2:]
	else:
		courses = courses[3:]
	for c in courses:
		if 'strong' in str(c):
			t = re.search(r'(JumpLink)?([\[\]\d\s]+)\.\s([^\d]+)\..+?\.\s(.+)', c.text)
			for key in FS_keys:
				if (re.search(key, str(t.group(3)), flags=re.IGNORECASE) or 
					re.search(key, str(t.group(4)), flags=re.IGNORECASE)):
					G_UG = 'UG'
					if re.search(r'^5', str(t.group(1))):
						G_UG = 'G'
					lab = False
					if (re.search(r'Laboratory|Lab', str(t.group(3)), 
						flags=re.IGNORECASE) or 
					re.search(r'Laboratory|Lab', str(t.group(4)), 
						flags=re.IGNORECASE)):
						lab = True
					csv_writer.writerow([dep_name, t.group(2), t.group(3), t.group(4), G_UG, form, lab, year, None, None, None])
	time.sleep(1)