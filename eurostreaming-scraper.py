#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup	# Used to get content from div could have used re though
import cfscrape		# Bypass cloudflare
import re			# Some regular expressions to carry out some readable data from html
import unshortenit

class Eurostreamingscraper():
	def __init__(self,query):
		self.query = query

	# Returns the urls found from the research issued
	def getUrls(self):
		url = "https://eurostreaming.club/?s="+self.query 
		scraper = cfscrape.create_scraper()
		data = scraper.get(url).content
	
		results = re.findall(r'<h2><a href="(https://eurostreaming\.club/.*?)" title="(.*?)">',data)
	
		return results

	# From the selected tv show url, get the link to the episodes list
	def getLinkspageUrl(self,url):
		scraper = cfscrape.create_scraper()
		data = scraper.get(url).content

		first_attempt = ''.join(re.findall(r'<a href="(.*?)"> &gt;&gt;',data))
		if first_attempt == '':
			return ''.join(re.findall(r'"go_to":"(.*?)"',data)).replace("\\","")
		return first_attempt

	# Attempts to get the clean url to the streaming by removing adfly and others shorteners
	def getClearUrl(self,url):
		try:
			un, status = unshortenit.unshorten_only(url)
			tmp = url.split("/","")
			if url != un or "vcrypt.net" not in tmp or "linkup.pro" not in tmp:
				return un
			un, status = unshortenit.unshorten(url)
			return un
		except:
			return url

	# Returns a list of dictionaries containing episode and its links -> {"episode_name" : name,"links": "link1 - link2 - link3"}
	def getData(self,url):
		results = []
		
		scraper = cfscrape.create_scraper()
		data = scraper.get(url).content
		doc = BeautifulSoup(data,"lxml")
		seasons = doc.findAll('div', {'class': 'su-spoiler-content su-clearfix',"style":"display:none"})
		for season in seasons:
			season = str(season).split("<br/>")
			for ep in season:
				try:
					tmplinks = re.findall(r'<a href="(.*?)"',ep)
					links = []
					for link in tmplinks:
						links.append(self.getClearUrl(link))
					
					res = {"episode":re.findall(r'([0-9]+.*?)–',ep)[0] ,"links":" - ".join(links)}
					results.append(res)
				except:
					pass
		return results

	# Returns the list of dictionaries from scratch
	def getEpisodes(self):
		results = self.getUrls()

		if len(results) == 0:
		 sys.exit("No results found.")

		for i in range(0,len(results)):
			print (str(i+1) +" - "+results[i][1])

		while True:
			choice = int(raw_input("Type the number of the movie/show you want: "))
			if choice>0 and choice<len(results)+1:
				break
			print("Invalid choice.")

		print("Getting links and obtaining clear urls..This may take up some time")

		return self.getData(self.getLinkspageUrl(results[choice-1][0]))

	# Print the list of results found
	def printEpisodes(self):
		eps = self.getEpisodes()
		print eps
		for ep in eps:
			print ep["episode"] +" - "+ep["links"]


query = raw_input("Show to look for: ")

eurostreaming = Eurostreamingscraper(query)
eurostreaming.printEpisodes()
