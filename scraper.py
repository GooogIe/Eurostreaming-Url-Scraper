#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup	# Used to get content from div could have used re though
import cfscrape		# Bypass cloudflare
import re			# Some regular expressions to carry out some readable data from html

print "Use this script to scrape any link to a streaming website from a specific movie/show on eurostreaming"
print "Paste the link of the page containing the episodes, not the page of the film/serie"
print "Not sure that this script works on EVERY page, should do it on almost every page"
url = raw_input("Paste the link: ")

scraper = cfscrape.create_scraper()

data = scraper.get(url).content

doc = BeautifulSoup(data)

seasons = doc.findAll('div', {'class': 'su-spoiler-content su-clearfix',"style":"display:none"})

for season in seasons:
	season = str(season).split("<br/>")
	for ep in season:
		try:
			string = re.findall(r'[0-9]+(.*?)–',ep)[0] +" - "+" - ".join(re.findall(r'<a href="(.*?)"',ep))
			print string
		except:
			pass
		
