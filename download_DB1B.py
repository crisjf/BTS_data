# Download DB1B data from:
# https://www.transtats.bts.gov/Tables.asp?DB_ID=125&DB_Name=Airline%20Origin%20and%20Destination%20Survey%20%28DB1B%29&DB_Short_Name=Origin%20and%20Destination%20Survey
# 
# Author: Cristian Jara-Figueroa
# Last modified: August 20th, 2020

import pandas as pd
import requests
import zipfile
from io import StringIO, BytesIO
import os

OUT_PATH = 'data'

def get_file(year,quarter):
	base_url = 'https://www.transtats.bts.gov/DownLoad_Table.asp'
	query = {
		'Table_ID':'272'
	}
	payload = {
		'UserTableName': 'DB1BTicket',
		'RawDataTable': 'T_DB1B_TICKET',
		'sqlstr':  f'SELECT YEAR,QUARTER,ORIGIN,ORIGIN_AIRPORT_ID,ORIGIN_AIRPORT_SEQ_ID,ORIGIN_CITY_MARKET_ID,ONLINE,REPORTING_CARRIER FROM  T_DB1B_TICKET WHERE Quarter ={quarter} AND YEAR={year}',
		'varlist': 'YEAR,QUARTER,ORIGIN,ORIGIN_AIRPORT_ID,ORIGIN_AIRPORT_SEQ_ID,ORIGIN_CITY_MARKET_ID,ONLINE,REPORTING_CARRIER',
		'time': f'Q {quarter}',
		'XYEAR': year,
	}

	r = requests.post(base_url,params=query,data=payload)
	return r

def extract_file(r,year,quarter):
	z = zipfile.ZipFile(BytesIO(r.content))
	for f in z.filelist:
		if 'T_DB1B_TICKET' in f.filename:
			z.extract(f.filename,path=OUT_PATH)
			os.rename(os.path.join(OUT_PATH,f.filename),os.path.join(OUT_PATH,f'{year}-{quarter}_'+f.filename))
	        
for year in range(1993,2021):
	if year<2020:
		quarters = range(1,5)
	elif year == 2020:
		quarters = [1]
	else:
		quarters = []
	for quarter in quarters:
		print(year,quarter)
		matching_files = [f for f in os.listdir(OUT_PATH) if ((f.split('_')[0] == f'{year}-{quarter}') & ('T_DB1B_TICKET' in f))]
		if len(matching_files)==0:
			r = get_file(year,quarter)
			extract_file(r,year,quarter)
		else:
			print('Found files:',matching_files)

print('END')