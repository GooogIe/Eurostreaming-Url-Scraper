#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup	# Used to get content from div could have used re though
import cfscrape		# Bypass cloudflare
import re			# Some regular expressions to carry out some readable data from html


def getUrls(query):
	url = "https://eurostreaming.club/?s="+query
	scraper = cfscrape.create_scraper()
	data = scraper.get(url).content
	
	results = re.findall(r'<h2><a href="(https://eurostreaming\.club/.*?)" title="(.*?)">',data)
	
	return results

def getLinkspageUrl(url):
	scraper = cfscrape.create_scraper()
	data = scraper.get(url).content

	first_attempt = ''.join(re.findall(r'<a href="(.*?)"> &gt;&gt;',data))
	if first_attempt == '':
		return ''.join(re.findall(r'"go_to":"(.*?)"',data)).replace("\\","")
	return first_attempt

def getData(url):
	results = []

	scraper = cfscrape.create_scraper()
	data = scraper.get(url).content
	doc = BeautifulSoup(data,"lxml")

	seasons = doc.findAll('div', {'class': 'su-spoiler-content su-clearfix',"style":"display:none"})
	for season in seasons:
		season = str(season).split("<br/>")
		for ep in season:
			try:
				string = re.findall(r'([0-9]+.*?)–',ep)[0] +" - "+" - ".join(re.findall(r'<a href="(.*?)"',ep))
				results.append(string)
			except:
				pass
	return results

query = raw_input("Show/movie to look for: ")

results = getUrls(query)

if len(results) == 0:
 sys.exit("No artist found")

for i in range(0,len(results)):
	print (str(i+1) +" - "+results[i][1])

while True:
	choice = int(raw_input("Type the number of the movie/show you want: "))
	if choice>0 and choice<len(results)+1:
		break
	print("Invalid choice.")

founds = getData(getLinkspageUrl(results[choice-1][0]))

for item in founds:
	print(item)
