import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.request
import csv

URL = 'http://catalog.okstate.edu/courses/#coursecatalogtext'
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
	p =  re.search(r'\/courses\/([^"#]+)', str(link))
	if p:
		departments.append("http://catalog.okstate.edu" + p.group(0))
	
some_dep = departments[3:8]
filename = "Oklahoma_State_University_Sample.csv"
csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Course Catalogue Number", "Department Name", "Course Name",
 "Course Description", "Graduate/Undergraduate", "Format", "Lab", 
 "Academic Catalogue Year", "Food Systems", "Food Justice/Equity",
 "Critical Pedagogy"])
FS_keys = ["agri", "food", "animal"]
#FJ_keys = ["conservation", "ethical"]
#CP_keys = ["communication", "discussion"]
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
		G_UG = None
		form = None
		lab = False
		title = course.find(class_="courseblocktitle").text
		desc = course.find(class_="courseblockdesc")
		if desc:
			desc = desc.text[13:]
		else:
			desc = "No Description"
		for key in FS_keys:
			if (re.search(key, title, flags=re.IGNORECASE) or 
				re.search(key, desc, flags=re.IGNORECASE)):
				t = re.search(r"([^\d]+)\s(\d+\w+)\s(.+)", title)
				extra = course.findAll(class_="courseblockextra")
				for e in extra:
					if "Levels" in e.text:
						G_UG = e.text[8:]
					if "Schedule types" in e.text:
						form = e.text[17:]
				if re.search(r'lab', form, flags=re.IGNORECASE):
					lab = True
				csv_writer.writerow([t.group(2), t.group(1), t.group(3), desc, 
					G_UG, form, lab, year, None, None, None])
	time.sleep(1)