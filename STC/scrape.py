import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import csv
import pandas as pd

# Generalizing note: maybe have a main url string variable
# and the course descriptions page string to add
# comes in handy in loop

URL = 'https://catalog.unh.edu/undergraduate/course-descriptions/'
page = requests.get(URL)

soup = BeautifulSoup(page.text, 'html.parser')
results = soup.findAll('a')

departments = [] #array of all department links
for link in results:
	#note: this actually filters and gets relevant links
	#but it may not be the best for generalizing
	p =  re.search(r'\/undergraduate\/course-descriptions\/([^"]+)', str(link))
	if p:
		departments.append("http://catalog.unh.edu" + p.group(0))
		# encode("utf-8") may help if error printing
	
	#note: this extracts all links - may be useful for generalization
	#but not the best for getting most useful links for the page
	#print(link.get('href'))

# Let's try on a few departments first
# department[4]: Agri Mech, 
# departments[8] : Animal Science,
# department[248] : Sustainable Agri & Food systems
# same idea as before:
departments_of_interest = [departments[4], departments[8], departments[248]]
filename = "UNH_all.csv"
csv_writer = csv.writer(open(filename, 'w'))
csv_writer.writerow(["Title", "Credit", "Attr", "Desc"])

full_keywords = []
# uncomment for all keywords:
#with open(r"keywords.txt", "r") as lines:
#	for line in lines:
#		if (line != "\n"):
#			if "\n" in line:
#				line = line.split("\n")[0]
#			full_keywords += [line]

keywords = ["agri", "agricultural", "food", "animal"] #for testing

# uncomment for all keywords:
# keywords = full_keywords

for dep in departments_of_interest:
	# when done tweaking code for specific school:
	# for dep in departments:
	URL = dep
	page = requests.get(URL)
	soup = BeautifulSoup(page.text, 'html.parser')
	# classes may differ across sites:
	courses = soup.findAll(class_="courseblock")
	for course in courses:
		title = course.find(class_="courseblocktitle").text
		check = course.findAll(class_="courseblockextra")
		attr = 'None'
		for c in check:
			if "Credit" in c.text:
				credit = c.text
			if "Attributes" in c.text:
				attr = c.text
	# this should work but it doesnt due to a classing error in the UNH system:
	# Use this for other schools if possible:
	# desc = course.find(class_="courseblockdesc").text
		desc = re.search(r'(<\/p>)\n([^<]+)', str(course)).group(2)
		for key in keywords: #filtered
			if (re.search(key, title, flags=re.IGNORECASE) or 
				re.search(key, desc, flags=re.IGNORECASE)):
				csv_writer.writerow([title, credit, attr, desc])