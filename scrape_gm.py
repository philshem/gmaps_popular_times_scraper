#!/usr/bin/env python

import os
import sys
import time
import urllib.parse
from selenium import webdriver
from bs4 import BeautifulSoup

# give time to download map tiles
SLEEP_SEC = 20.0
DELIM = ','

# gmaps starts their weeks on sunday
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def main():
	if len(sys.argv) > 1:
		url = sys.argv[1]
	else:
		# if no URL is given on the command line, use a default one 🌯
		url = 'https://www.google.com/maps/place/Der+Gr%C3%BCne+Libanon/@47.3809042,8.5325368,17z/data=!3m1!4b1!4m5!3m4!1s0x47900a0e662015b7:0x54fec14b60b7f528!8m2!3d47.3809006!4d8.5347255'
		#url = 'https://www.google.com/maps/place/Kosmos/@47.3799843,8.526892,17z/data=!4m12!1m6!3m5!1s0x47900a1a13199a79:0xe6f55badfe01aaf1!2sKosmos!8m2!3d47.3799807!4d8.5290807!3m4!1s0x47900a1a13199a79:0xe6f55badfe01aaf1!8m2!3d47.3799807!4d8.5290807'
		#url = 'https://www.google.com/maps/place/Weinkeller+Z%C3%BCrich-Enge,+M%C3%B6venpick+Schweiz+AG,+Division+Wein/@47.3557346,8.5296615,17z/data=!3m1!4b1!4m5!3m4!1s0x479009e36fcc338b:0xe6cda6cfb0833802!8m2!3d47.355731!4d8.5318502'
	
	# generate filename from gmaps url
	try:
		file_name = url.split('/')[5].split(',')[0]
		file_name = urllib.parse.unquote(file_name).replace('+','_')
	except:
		# maybe the URL is a short one, or whatever
		file_name = url.split('/')[-1]
		file_name = urllib.parse.unquote(file_name).replace('+','_')
	#print(file_name)
	
	# get html source (note this uses headless Chrome via Selenium)
	html = get_html(url, 'html' + os.sep + file_name+'.html')

	# parse html (uses beautifulsoup4)
	data = parse_html(html)
	
	# print header
	print(DELIM.join(('place','day of week', 'hour of day', 'popularity (%)')))
	
	# print csv
	for row in data:
		print(file_name+DELIM + DELIM.join([str(x) for x in row]))


def get_html(url,file_name):

	# if the html source exists as a local file, don't bother to scrape it
	if os.path.isfile(file_name):
		with open(file_name,'r') as f:
			html = f.read()
		return html

	else:
		# requires chromedriver
		options = webdriver.ChromeOptions()
		#options.add_argument('--start-maximized')
		options.add_argument('--headless')
		# https://stackoverflow.com/a/55152213/2327328
		# I choose German because the time is 24h, less to parse
		options.add_argument('--lang=de-DE')
		options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
		chrome_driver_binary = '/usr/local/bin/chromedriver'
		d = webdriver.Chrome(chrome_driver_binary, options=options)

		# get page
		d.get(url)

		# sleep to let the page render, it can take some time
		time.sleep(SLEEP_SEC)

		# save html local file
		with open(file_name, 'w') as f:
			f.write(d.page_source)

		# save html as variable
		html = d.page_source

		d.quit()
		return html

def parse_html(html):

	soup = BeautifulSoup(html,features='html.parser')

	pops = soup.find_all('div', {'class': 'section-popular-times-bar'})
	
	hour = 0
	dow = 0
	data = []

	for pop in pops:
		# note that data is stored sunday first, regardless of the local
		t = pop['aria-label']
		#print(t)

		hour_prev = hour

		try:
			if 'normal' not in t:
				hour = int(t.split()[1])
				freq = int(t.split()[4]) # gm uses int
			else:
				# the current hour has special text
				# hour is the previous value + 1
				hour = hour + 1
				freq = int(t.split()[-2])
			
			if hour < hour_prev:
				# increment the day if the hour decreases
				dow += 1

			data.append([days[dow % 7], hour, freq])
			# could also store an array of dictionaries
			#data.append({'day' : days[dow % 7], 'hour' : hour, 'popularity' : freq})

		except:
			# if a day is missing, the line(s) won't be parsable
			# this can happen if the place is closed on that day
			# skip them, hope it's only 1 day per line, 
			# and increment the day counter
			dow += 1

	return data




if __name__ == '__main__':
	main()