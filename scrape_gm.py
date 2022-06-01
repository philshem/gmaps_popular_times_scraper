#!/usr/bin/env python

'''
Run the google maps popularity scraper
'''

import os
import sys
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# load local params from config.py
import config

# gmaps starts their weeks on sunday
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# generate unique runtime for this job
run_time = datetime.now().strftime('%Y%m%d_%H%M%S')

def main():
	# read the list of URLs from a URL, or path to a local csv
	if not config.DEBUG:
		if len(sys.argv) > 1:
			# read path to file from system arguments
			urls = pd.read_csv(sys.argv[1])
		else:
			# get path to file from config.py
			urls = pd.read_csv(config.URL_PATH_INPUT)
	else:
		# debugging case
		print('RUNNING TEST URLS...')
		urls = pd.read_csv(config.URL_PATH_INPUT_TEST)

	# write to folder logs to remember the state of the config file
	urls.to_csv('logs' + os.sep + run_time + '.log', index = False)

	url_list = urls.iloc[:, 0].tolist()
	for url in url_list:
		#print(urllib.parse.urlparse(url))
		#print (url)

		try:
			data = run_scraper(url)
		except:
			print('ERROR:', url, run_time)
			# go to next url
			continue

		if len(data) > 0:
			# valid data to be written
			file_name = make_file_name(url)

			with open('data' + os.sep + file_name + '.' + run_time + '.csv', 'w') as f:
				# write header
				f.write(config.DELIM.join(config.HEADER_COLUMNS)+'\n')

				# write data
				for row in data:
					f.write(config.DELIM.join((file_name,url,run_time)) + config.DELIM + config.DELIM.join([str(x or '') for x in row])+'\n')

			print('DONE:', url, run_time)

		else:
			print('WARNING: no data', url, run_time)

def run_scraper(u):

	# because scraping takes some time, write the actual timestamp instead of the runtime
	scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	# get html source (note this uses headless Chrome via Selenium)
	html = get_html(u, 'html' + os.sep + make_file_name(u) + '.' + run_time + '.html')

	# parse html (uses beautifulsoup4)
	data = parse_html(html)

	return data

def make_file_name(u):
	# generate filename from gmaps url
	# TODO - maybe clean this up

	try:
		file_name = u.split('/')[5].split(',')[0]
		file_name = urllib.parse.unquote(file_name).replace('+','_').replace('?','_')
	except:
		# maybe the URL is a short one, or whatever
		file_name = u.split('/')[-1]
		file_name = urllib.parse.unquote(file_name).replace('+','_').replace('?','_')
	#print(file_name)

	#file_name = file_name + '.' + run_time

	return file_name

def get_html(u,file_name):

	# if the html source exists as a local file, don't bother to scrape it
	# this shouldn't run
	if False and os.path.isfile(file_name):
		with open(file_name,'r') as f:
			html = f.read()
		return html

	else:
		if config.REMOTE_CHROME_URL != '':
			d = webdriver.Remote(config.REMOTE_CHROME_URL, DesiredCapabilities.CHROME)
		else:
			# requires chromedriver
			options = webdriver.ChromeOptions()
			#options.add_argument('--start-maximized')
			options.add_argument('--headless')
			# https://stackoverflow.com/a/55152213/2327328
			# I choose German because the time is 24h, less to parse
			options.add_argument('--lang=de-DE')
			options.binary_location = config.CHROME_BINARY_LOCATION
			chrome_driver_binary = config.CHROMEDRIVER_BINARY_LOCATION
			d = webdriver.Chrome(chrome_driver_binary, options=options)

		# get page
		d.get(u)

		# sleep to let the page render, it can take some time
		# timeout after max N seconds (config.py)
		# based on https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
		try:
			WebDriverWait(d, config.SLEEP_SEC).until(EC.presence_of_element_located((By.CLASS_NAME, 'C7xf8b')))
		except TimeoutException:
			print('ERROR: Timeout! (This could be due to missing "popular times" data, or not enough waiting.)',u)

		# save html local file
		if config.SAVE_HTML:
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
		# debugging
		#print(t)

		hour_prev = hour
		freq_now = None

		try:
			if 'normal' not in t:
				hour = int(t.split()[1])
				freq = int(t.split()[4]) # gm uses int
			else:
				# the current hour has special text
				# hour is the previous value + 1
				hour = hour + 1
				freq = int(t.split()[-2])

				# gmaps gives the current popularity,
				# but only the current hour has it
				try:
					freq_now = int(t.split()[2])
				except:
					freq_now = None

			if hour < hour_prev:
				# increment the day if the hour decreases
				dow += 1

			data.append([days[dow % 7], hour, freq, freq_now])
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
