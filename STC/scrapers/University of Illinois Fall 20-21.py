import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.request
import csv

URL = 'http://catalog.illinois.edu/courses-of-instruction/'
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = []
for link in results:
	p =  re.search(r'\/courses-of-instruction\/([^"#]+)', str(link))
	if p:
		departments.append("http://catalog.illinois.edu" + p.group(0))
	
some_dep = departments[3:8]
filename = "University_of_Illinois_Sample.csv"
csv_writer = csv.writer(open(filename, 'w', encoding='utf-8'))
csv_writer.writerow(["Department Name", "Course Catalogue Number", 
	"Course Name", "Course Description", "Graduate/Undergraduate", "Format", "Lab", 
 "Academic Catalogue Year", "Food Systems", "Food Justice/Equity",
 "Critical Pedagogy"])
FS_keys = ["agri", "food", "animal"]
#FJ_keys = ["conservation", "ethical"]
#CP_keys = ["communication", "discussion"]
year = "2020-2021"
form = None
lab = None
#FS = False
#FJ = False
#CP = False

for dep in some_dep:
	URL = dep
	page = requests.get(URL)
	soup = BeautifulSoup(page.text, 'html.parser')
	dep_name = soup.find('h1').text

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
				t = re.search(r"[^\d]+\s(\d+)\s(.+)credit.+", title)
				G_UG = "UG"
				if int(t.group(1)) >= 500:
					G_UG = "G"
				lab = False
				if (re.search(r'Laboratory|Lab', title, 
					flags=re.IGNORECASE) or 
				re.search(r'Laboratory|Lab', desc, 
					flags=re.IGNORECASE)):
					lab = True
				csv_writer.writerow([dep_name, t.group(1), 
					t.group(2)[2:-4], desc, G_UG, form, lab, 
					year, None, None, None])
	time.sleep(1)