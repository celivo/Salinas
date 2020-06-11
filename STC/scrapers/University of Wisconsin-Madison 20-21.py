import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.request
import csv

URL = 'https://guide.wisc.edu/courses/'
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
	p =  re.search(r'\/courses\/([^"#]+)', str(link))
	if p:
		departments.append("https://guide.wisc.edu" + p.group(0))
	
some_dep = departments[3:8]
filename = "University_of_Wisconsin_Madison_Sample.csv"
csv_writer = csv.writer(open(filename, 'w', encoding="utf-8"))
csv_writer.writerow(["Course Catalogue Number", "Department Name", "Course Name",
 "Course Description", "Graduate/Undergraduate", "Format", "Lab", 
 "Academic Catalogue Year", "Food Systems", "Food Justice/Equity",
 "Critical Pedagogy"])
FS_keys = ["agri", "food", "animal"]
#FJ_keys = ["conservation", "ethical"]
#CP_keys = ["communication", "discussion"]
year = "2020-2021"
form = None
lab = None
G_UG = None
#FS = False
#FJ = False
#CP = False

for dep in some_dep:
	URL = dep
	page = requests.get(URL)
	soup = BeautifulSoup(page.text, 'html.parser')
	soup.encode("utf-8")

	courses = soup.findAll(class_="courseblock")
	for course in courses:
		title = course.find(class_="courseblocktitle").text
		desc = course.find(class_="courseblockdesc")
		if desc:
			desc = desc.text
		else:
			desc = "No Description"
		for key in FS_keys:
			if (re.search(key, title, flags=re.IGNORECASE) or 
				re.search(key, desc, flags=re.IGNORECASE)):
				t = re.search(r"([^\d]+)\s(\d+\w*)\s.\s(.+)", title)
				csv_writer.writerow([t.group(2), t.group(1), t.group(3), desc, 
					G_UG, form, lab, year, None, None, None])
	time.sleep(1)