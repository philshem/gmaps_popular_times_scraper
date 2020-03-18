#!/usr/bin/env python

'''
Convert all CSVs to one big db or csv
'''

import os
import glob
import pandas as pd
import sqlite3

def main():
	# get all matching csv files
	all_files = glob.glob('data' + os.sep + '*.csv')
	
	# it's not big data
	# and they should have all the same data model
	df = pd.concat((pd.read_csv(f) for f in all_files))

	conn = sqlite3.connect('data' + os.sep + 'all.sqlite')
	df.to_sql(name='all', con=conn, if_exists='replace', index=False)

	conn.close()

if __name__ == '__main__':
	main()